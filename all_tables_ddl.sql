-- Таблица: users
CREATE TABLE [users] (
  [id] INT NOT NULL,
  [name] NVARCHAR(100) NOT NULL,
  [email] NVARCHAR(MAX) NULL,
  [created_at] DATETIME2 NULL,
  CONSTRAINT [PK_users] PRIMARY KEY ([id])
);

