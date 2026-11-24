-- =====================================================================================
-- Wellspace: SQL for the JOIN and SUBQUERY implementations
-- Run these in the Supabase SQL Editor. Replace 1 with a real auth_user id
-- (find one with:  SELECT id, email FROM auth_user;)
-- These are the same statements Django generates (see: python manage.py show_sql)
-- =====================================================================================

-- ---------- 1. JOIN : check-in history (4 tables) ------------------------------------
-- Main table: surveys_answer      Related: surveys_question, surveys_surveyresponse, surveys_survey
-- Foreign keys: answer.question_id -> question.id, answer.response_id -> response.id,
--               response.survey_id -> survey.id          (all One-to-Many)
SELECT r.week_start,
       r.submitted_at,
       s.title      AS survey,
       q.text       AS question,
       q.answer_type,
       a.value      AS answer
FROM surveys_answer a
INNER JOIN surveys_question       q ON a.question_id = q.id
INNER JOIN surveys_surveyresponse r ON a.response_id = r.id
INNER JOIN surveys_survey         s ON r.survey_id   = s.id
WHERE r.user_id = 1
ORDER BY r.week_start DESC, r.id, q.id;


-- ---------- 2. SUBQUERY : check-ins where the user reported discomfort ---------------
-- Inner query : ids of check-ins that contain a "Yes" to a yes/no question
-- Outer query : this user's check-ins whose id is in the inner result
SELECT r.id, r.week_start, s.title
FROM surveys_surveyresponse r
INNER JOIN surveys_survey s ON r.survey_id = s.id
WHERE r.user_id = 1
  AND r.id IN (
        SELECT a.response_id                         -- inner query
        FROM surveys_answer a
        INNER JOIN surveys_question q ON a.question_id = q.id
        WHERE q.answer_type = 3                      -- 3 = yes/no question
          AND a.value = 'true'                       -- answered "Yes"
  )
ORDER BY r.week_start DESC;


-- ---------- 3. Verification helpers (for the demo video) -----------------------------
-- Run the inner query alone to show what it returns:
SELECT a.response_id
FROM surveys_answer a
INNER JOIN surveys_question q ON a.question_id = q.id
WHERE q.answer_type = 3 AND a.value = 'true';

-- Show the foreign keys that connect the tables (the relationships):
SELECT conrelid::regclass AS table_name, conname AS constraint_name,
       pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE contype = 'f'
  AND conrelid::regclass::text IN ('surveys_answer','surveys_surveyresponse');
