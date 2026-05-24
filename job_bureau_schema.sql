-- ============================================================
--  Job Bureau Platform — Database Schema
--  СУБД: MariaDB 10.6+
--  Кодировка: utf8mb4 / utf8mb4_unicode_ci
-- ============================================================

CREATE DATABASE IF NOT EXISTS job_bureau
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE job_bureau;

-- ============================================================
-- 1. ПОЛЬЗОВАТЕЛИ (единая таблица аутентификации)
-- ============================================================
CREATE TABLE users (
    id            BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    email         VARCHAR(255)     NOT NULL,
    password_hash VARCHAR(255)     NOT NULL,
    role          ENUM('applicant','employer') NOT NULL,
    is_verified   TINYINT(1)       NOT NULL DEFAULT 0,   -- 0=Нет, 1=Да
    created_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                            ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;


-- ============================================================
-- 2. СОИСКАТЕЛИ
-- ============================================================
CREATE TABLE applicants (
    id            BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    user_id       BIGINT UNSIGNED  NOT NULL,

    -- Личные данные
    last_name     VARCHAR(100)     NOT NULL,
    first_name    VARCHAR(100)     NOT NULL,
    middle_name   VARCHAR(100)         NULL,
    date_of_birth DATE                 NULL,
    gender        ENUM('male','female','other') NULL,
    phone         VARCHAR(30)          NULL,
    avatar        VARCHAR(500)         NULL,  -- путь/URL к фото

    -- Местоположение
    country       VARCHAR(100)         NULL,
    city          VARCHAR(100)         NULL,
    address       VARCHAR(255)         NULL,

    -- Профиль
    about         TEXT                 NULL,
    status        ENUM(
                    'actively_looking',   -- активно ищет
                    'open_to_offers',     -- рассматривает предложения
                    'not_looking'         -- не ищет
                  ) NOT NULL DEFAULT 'actively_looking',

    created_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                            ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_applicants_user (user_id),
    CONSTRAINT fk_applicants_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 3. ПАСПОРТА СОИСКАТЕЛЕЙ
-- ============================================================
CREATE TABLE applicant_passports (
    id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    applicant_id BIGINT UNSIGNED NOT NULL,
    series       VARCHAR(20)         NULL,
    number       VARCHAR(30)     NOT NULL,
    scan         VARCHAR(500)        NULL,  -- путь/URL к скану
    created_at   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                                           ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_passport_applicant (applicant_id),
    CONSTRAINT fk_passport_applicant
        FOREIGN KEY (applicant_id) REFERENCES applicants(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 4. ТРУДОВЫЕ КНИЖКИ СОИСКАТЕЛЕЙ
-- ============================================================
CREATE TABLE applicant_work_books (
    id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    applicant_id BIGINT UNSIGNED NOT NULL,
    number       VARCHAR(30)     NOT NULL,
    scan         VARCHAR(500)        NULL,  -- путь/URL к скану
    created_at   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                                           ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_workbook_applicant (applicant_id),
    CONSTRAINT fk_workbook_applicant
        FOREIGN KEY (applicant_id) REFERENCES applicants(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 5. РЕЗЮМЕ СОИСКАТЕЛЕЙ
--    Один соискатель — несколько резюме (по должностям)
-- ============================================================
CREATE TABLE resumes (
    id             BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    applicant_id   BIGINT UNSIGNED  NOT NULL,

    title          VARCHAR(255)     NOT NULL,  -- желаемая должность
    experience_years TINYINT UNSIGNED NOT NULL DEFAULT 0,
    salary_expected  DECIMAL(12,2)      NULL,  -- желаемая ЗП
    education      ENUM(
                     'no_education',
                     'secondary',
                     'vocational',
                     'incomplete_higher',
                     'bachelor',
                     'master',
                     'phd'
                   )                   NULL,
    skills         TEXT                NULL,  -- ключевые навыки (теги через запятую)
    resume_pdf     VARCHAR(500)        NULL,  -- путь/URL к PDF-файлу
    status         ENUM(
                     'active',    -- активное, видно работодателям
                     'hidden',    -- скрытое
                     'archived'   -- в архиве
                   ) NOT NULL DEFAULT 'active',

    created_at     DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                             ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_resumes_applicant
        FOREIGN KEY (applicant_id) REFERENCES applicants(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 6. РАБОТОДАТЕЛИ
-- ============================================================
CREATE TABLE employers (
    id              BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED  NOT NULL,

    -- Основные данные
    company_name    VARCHAR(255)     NOT NULL,
    inn             VARCHAR(20)          NULL,
    industry        VARCHAR(150)         NULL,  -- сфера деятельности
    founded_year    YEAR                 NULL,  -- год основания
    website         VARCHAR(500)         NULL,
    logo            VARCHAR(500)         NULL,  -- путь/URL к лого
    about           TEXT                 NULL,
    is_verified     TINYINT(1)       NOT NULL DEFAULT 0,  -- 0=Нет, 1=Да

    -- Контакт
    phone           VARCHAR(30)          NULL,
    contact_person  VARCHAR(255)         NULL,  -- имя контактного лица

    -- Местоположение
    country         VARCHAR(100)         NULL,
    city            VARCHAR(100)         NULL,
    address         VARCHAR(255)         NULL,

    created_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                              ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_employers_user (user_id),
    UNIQUE KEY uq_employers_inn  (inn),
    CONSTRAINT fk_employers_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 7. ВАКАНСИИ
-- ============================================================
CREATE TABLE vacancies (
    id               BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    employer_id      BIGINT UNSIGNED  NOT NULL,

    title            VARCHAR(255)     NOT NULL,
    about            TEXT                 NULL,
    experience_years TINYINT UNSIGNED NOT NULL DEFAULT 0,
    salary_min       DECIMAL(12,2)        NULL,
    salary_max       DECIMAL(12,2)        NULL,

    employment_type  ENUM(
                       'full_time',
                       'part_time',
                       'internship',
                       'contract',
                       'freelance'
                     ) NOT NULL DEFAULT 'full_time',

    schedule         ENUM(
                       'five_days',     -- пятидневка
                       'shift',         -- сменный
                       'flexible',      -- гибкий
                       'remote'         -- удалённый
                     ) NOT NULL DEFAULT 'five_days',

    work_format      ENUM(
                       'office',
                       'remote',
                       'hybrid'
                     ) NOT NULL DEFAULT 'office',

    -- Местоположение
    country          VARCHAR(100)         NULL,
    city             VARCHAR(100)         NULL,
    address          VARCHAR(255)         NULL,

    -- Контактные данные по вакансии
    contact_name     VARCHAR(255)         NULL,
    contact_phone    VARCHAR(30)          NULL,
    contact_email    VARCHAR(255)         NULL,

    status           ENUM(
                       'active',
                       'paused',
                       'closed'
                     ) NOT NULL DEFAULT 'active',

    expires_at       DATE                 NULL,  -- дата истечения вакансии
    created_at       DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                              ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_vacancies_employer
        FOREIGN KEY (employer_id) REFERENCES employers(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- 8. ОТКЛИКИ
-- ============================================================
CREATE TABLE applications (
    id               BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    vacancy_id       BIGINT UNSIGNED  NOT NULL,
    resume_id        BIGINT UNSIGNED  NOT NULL,

    cover_letter     TEXT                 NULL,  -- сопроводительное письмо

    status           ENUM(
                       'pending',    -- ожидает рассмотрения
                       'viewed',     -- просмотрено работодателем
                       'accepted',   -- приглашение
                       'rejected'    -- отказ
                     ) NOT NULL DEFAULT 'pending',

    employer_comment TEXT                 NULL,  -- обоснование решения работодателя

    created_at       DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                              ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    -- Один соискатель не может откликнуться на одну вакансию дважды
    UNIQUE KEY uq_application (vacancy_id, resume_id),
    CONSTRAINT fk_applications_vacancy
        FOREIGN KEY (vacancy_id) REFERENCES vacancies(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_applications_resume
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================
-- ИНДЕКСЫ ДЛЯ ЧАСТЫХ ЗАПРОСОВ
-- ============================================================

-- Поиск вакансий по городу, статусу, формату
CREATE INDEX idx_vacancies_city       ON vacancies (city);
CREATE INDEX idx_vacancies_status     ON vacancies (status);
CREATE INDEX idx_vacancies_work_format ON vacancies (work_format);
CREATE INDEX idx_vacancies_employer   ON vacancies (employer_id);

-- Поиск резюме по статусу и специализации
CREATE INDEX idx_resumes_applicant    ON resumes (applicant_id);
CREATE INDEX idx_resumes_status       ON resumes (status);

-- Отклики: быстрый поиск по вакансии и резюме
CREATE INDEX idx_applications_vacancy ON applications (vacancy_id);
CREATE INDEX idx_applications_resume  ON applications (resume_id);
CREATE INDEX idx_applications_status  ON applications (status);

-- Соискатели: фильтрация по городу и статусу поиска работы
CREATE INDEX idx_applicants_city      ON applicants (city);
CREATE INDEX idx_applicants_status    ON applicants (status);
