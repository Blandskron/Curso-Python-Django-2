CREATE OR REPLACE FUNCTION trg_enrollments_audit()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    -- (Opcional) validar curso activo al matricular
    IF NOT EXISTS (
      SELECT 1 FROM courses c
      WHERE c.course_id = NEW.course_id
        AND c.is_active = TRUE
    ) THEN
      RAISE EXCEPTION 'No se puede matricular: el curso % no está activo', NEW.course_id;
    END IF;

    INSERT INTO enrollment_history(
      event_type, student_id, course_id,
      old_status, new_status,
      old_grade, new_grade,
      details
    )
    VALUES (
      'ENROLL', NEW.student_id, NEW.course_id,
      NULL, NEW.status,
      NULL, NEW.final_grade,
      jsonb_build_object('enrolled_at', NEW.enrolled_at)
    );

    RETURN NEW;
  ELSIF TG_OP = 'UPDATE' THEN
    -- (Opcional) exigir nota cuando se completa
    -- IF NEW.status = 'COMPLETED' AND NEW.final_grade IS NULL THEN
    --   RAISE EXCEPTION 'Si status=COMPLETED debes informar final_grade';
    -- END IF;

    -- Si el curso está inactivo, no permitir volver a ACTIVE/COMPLETED
    IF EXISTS (
      SELECT 1 FROM courses c
      WHERE c.course_id = NEW.course_id
        AND c.is_active = FALSE
    ) AND NEW.status IN ('ACTIVE','COMPLETED') THEN
      RAISE EXCEPTION 'No se puede dejar %: el curso % está inactivo', NEW.status, NEW.course_id;
    END IF;

    -- Registrar solo si hubo cambios relevantes
    IF (OLD.status IS DISTINCT FROM NEW.status)
       OR (OLD.final_grade IS DISTINCT FROM NEW.final_grade) THEN

      INSERT INTO enrollment_history(
        event_type, student_id, course_id,
        old_status, new_status,
        old_grade, new_grade,
        details
      )
      VALUES (
        'UPDATE', NEW.student_id, NEW.course_id,
        OLD.status, NEW.status,
        OLD.final_grade, NEW.final_grade,
        jsonb_build_object(
          'old_enrolled_at', OLD.enrolled_at,
          'new_enrolled_at', NEW.enrolled_at
        )
      );
    END IF;

    RETURN NEW;
  ELSE
    -- DELETE
    INSERT INTO enrollment_history(
      event_type, student_id, course_id,
      old_status, new_status,
      old_grade, new_grade,
      details
    )
    VALUES (
      'UNENROLL', OLD.student_id, OLD.course_id,
      OLD.status, NULL,
      OLD.final_grade, NULL,
      jsonb_build_object('enrolled_at', OLD.enrolled_at)
    );

    RETURN OLD;
  END IF;
END;
$$;

DROP TRIGGER IF EXISTS enrollments_audit_trg ON enrollments;

CREATE TRIGGER enrollments_audit_trg
AFTER INSERT OR UPDATE OR DELETE ON enrollments
FOR EACH ROW
EXECUTE FUNCTION trg_enrollments_audit();


CREATE OR REPLACE FUNCTION trg_courses_on_deactivate()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- Solo cuando se cambia de activo -> inactivo
  IF (OLD.is_active = TRUE AND NEW.is_active = FALSE) THEN
    UPDATE enrollments e
       SET status = 'DROPPED',
           final_grade = NULL
     WHERE e.course_id = NEW.course_id
       AND e.status = 'ACTIVE';
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS courses_deactivate_trg ON courses;

CREATE TRIGGER courses_deactivate_trg
AFTER UPDATE OF is_active ON courses
FOR EACH ROW
EXECUTE FUNCTION trg_courses_on_deactivate();

