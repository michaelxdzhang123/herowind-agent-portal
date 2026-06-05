# AGENTS.md

## Objective

Build a small web interface that lets an administrator:

1. Log in through a login page.
2. Create a new user.
3. Generate an API key for that user.
4. Save the user record and API key to a local JSON file which ia already in here named keys.json 

Use a JSON file for storage. Do not use a database unless the user explicitly asks for one later.

> Note: The user described the storage file as a "JASN" file. Treat this as `JSON`.

## Required UI

### Login page
 use static/css/login.css

The login page should include:

- Username field.
- Password field.
- Login button.
- Basic error message area.
- a logo named: HeroGateway

The page body should use:

```html
<body class="signin">
```

The login form should be placed inside a container using:

```html
<div class="signinpanel">
```

### User management page

After login, show a simple user management page where the administrator can:

- Enter a username.
- Enter an optional display name or email.
- Click a button to generate an API key.
- Save the new user to the JSON file.
- View a list of existing users.

Do not display full API keys in the user list by default. Show only a masked version, for example:

```text
hero_1234****************abcd
```

Provide a way to copy the full API key immediately after creation.

## Storage Requirements

Store users in a JSON file. Use this default filename unless the project already has a better storage location:

```text
data/keys.json
```

Create the `data` directory automatically if it does not exist.

The JSON file should use structure in file: data/keys.json


Prefer hashing API keys if practical. If plaintext storage is used, clearly document that this is only suitable for local development or trusted internal tools.

## API Key Requirements

Generated API keys should:

- Be unique.
- Be difficult to guess.
- Use a clear prefix, such as `hero_`.
- Be generated using a cryptographically secure random function.
- Be shown to the administrator once at creation time.

Example format:

```text
hero_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Do not generate API keys using predictable values such as usernames, dates, counters, or `Math.random()`.

## Validation Requirements

Validate all user input before saving.

Required validation:

- Username is required.
- Username must be unique.
- Username should contain only letters, numbers, hyphens, underscores, or dots.

Return clear error messages in the web interface.

## File Handling Requirements

When writing to the JSON file:

- Read the current file contents first.
- Parse the existing JSON safely.
- Handle missing or empty files.
- Write valid, pretty-printed JSON.
- Avoid corrupting the file if a write fails.
- Use atomic writes when possible by writing to a temporary file first, then renaming it.

Example save flow:

1. Ensure `data/keys.json` exists.
2. Load current users.
3. Validate the new user.
4. Add the new user.
5. Write to `data/keys.json.tmp`.
6. Rename `data/keys.json.tmp` to `data/keys.json`.

## Authentication Requirements

Implement a simple admin login for the web interface.

For local development, admin credentials may come from environment variables:

```text
ADMIN_USERNAME=admin
ADMIN_PASSWORD=stone11031103
```

Do not hardcode production passwords in source code.

The login page should redirect authenticated users to the user management page.

Unauthenticated users should not be able to create users or API keys.

## Suggested Routes

Use these routes unless the existing project structure requires different names:

```text
GET  /login        Show login page
POST /login        Authenticate admin
POST /logout       End admin session
GET  /users        Show user management page
POST /users        Create user and API key
GET  /api/users    Return existing users with masked API keys only
```

Never return full API keys from list endpoints.

## Suggested Project Structure

Use this structure for a small app if no project structure exists yet:

```text
.
├── AGENTS.md
├── data/
│   └── keys.json
├── static/
│   └── css/
│       └── login.css
├── src/
│   ├── server.*
│   ├── routes/
│   │   ├── auth.*
│   │   └── users.*
│   ├── services/
│   │   ├── apiKeys.*
│   │   └── userStore.*
│   └── templates/
│       ├── login.*
│       └── users.*
└── package.json / requirements.txt / equivalent
```

If the uploaded `login.css` is currently outside the project, copy it into:


Then reference it from the login page with:

<link rel="stylesheet" href="static/css/login.css">
```

The provided CSS references image paths such as:

```text
../img/login-background.jpg
../img/user.png
../img/locked.png
```

## Security Notes

This project handles API keys, so treat them as secrets.

Minimum security expectations:

- Do not log full API keys.
- Do not display full API keys after the creation confirmation screen.
- Do not commit real API keys to version control.
- Use HTTPS in production.
- Use secure session cookies in production.
- Keep the JSON file outside any public/static folder.
- Restrict file permissions for `data/keys.json` where possible.

## Acceptance Criteria

The task is complete when:

- A login page exists and uses `templates/login.html`.
- Admin login works.
- Authenticated admin users can open the user management page.
- Admin users can create a username and generate an API key.
- New users are saved to `data/keys.json`.
- Existing users can be listed with masked API keys.
- Duplicate usernames are rejected.
- API keys are generated securely.
- The app handles a missing `data/keys.json` file gracefully.
- The JSON file remains valid after creating users.

## Testing Checklist

Test these cases before finishing:

- Login page loads with `login.html`.
- Login fails with wrong credentials.
- Login succeeds with correct credentials.
- User creation fails when username is empty.
- User creation fails when username already exists.
- User creation succeeds with a valid username.
- API key is shown once after creation.
- User list shows masked API keys only.
- `data/keys.json` contains valid JSON after saving.
- Restarting the app still loads existing users from the JSON file.

## Implementation Preference

Keep the implementation simple and easy to run locally. Favor readable code over complex abstractions.

Do not add unnecessary frameworks, database systems, or external services unless required by the existing project.
