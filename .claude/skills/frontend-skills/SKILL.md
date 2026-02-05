```markdown
# Frontend Skill – Complete Definition


**Frontend Skill** is a specialized capability focused on building the **Next.js App Router frontend** for the Phase II Todo Full-Stack Web Application. When invoked, this skill provides expertise in UI layout, React/Next.js component design, Tailwind CSS styling, Better Auth integration, and secure communication with the FastAPI backend for the hackathon todo application.[file:55][web:5][web:56][web:62]


---


## Table of Contents


1. [Skill Purpose](#skill-purpose)  
2. [Project-Specific Context](#project-specific-context)  
3. [Core Components](#core-components)  
   - [Page & Route Structure](#1-page--route-structure)  
   - [Authentication Flows](#2-authentication-flows)  
   - [API Client Integration](#3-api-client-integration)  
   - [Task Management UI](#4-task-management-ui)  
   - [State Management & Data Fetching](#5-state-management--data-fetching)  
   - [Form Handling & Validation](#6-form-handling--validation)  
   - [Responsive Layout & Styling](#7-responsive-layout--styling)  
   - [Error & Loading States](#8-error--loading-states)  
   - [Frontend Security Practices](#9-frontend-security-practices)  
   - [Accessibility & UX](#10-accessibility--ux)  
4. [When to Invoke Frontend Skill](#when-to-invoke-frontend-skill)  
5. [How Frontend Skill Works](#how-frontend-skill-works)  
6. [Frontend Skill Output](#frontend-skill-output)  
7. [Implementation Patterns](#implementation-patterns)  
8. [Phase II–Specific Rules](#phase-ii–specific-rules)  
9. [Troubleshooting Guide](#troubleshooting-guide)  


---


## Skill Purpose


Frontend Skill enables you to design and implement the **user interface** and **client-side behavior** of the todo application using **Next.js (App Router), TypeScript, and Tailwind CSS**, integrated with Better Auth and the FastAPI backend.

It covers:

- Routing and page layout with the Next.js App Router  
- Auth UI (signin/signup) wired to Better Auth  
- API client usage to call FastAPI endpoints with JWT  
- Rendering and interacting with the task list (CRUD + complete)  
- Responsive, accessible, and clean UI design  
- Proper handling of loading, error, and empty states  
- Basic client-side validation to complement backend validation

This skill ensures that the frontend is coherent with the spec, easy to use, and correctly integrated with the auth and backend layers.[file:55][web:5]


---


## Project-Specific Context


Frontend Skill operates within **Phase II – Todo Full-Stack Web Application** using these technologies:[file:55]

### Technology Stack


| Layer     | Technology          | Purpose                                     |
|----------|---------------------|---------------------------------------------|
| Frontend | Next.js 16+ (App Router) | UI and routing framework (React-based) |
| Language | TypeScript          | Type-safe frontend code                     |
| Styling  | Tailwind CSS        | Utility-first styling                       |
| Auth     | Better Auth         | Signup/signin, session, JWT issuance        |
| Backend  | FastAPI             | REST API for tasks                          |[web:5][web:62]


### Frontend Project Structure


```text
frontend/
├── app/
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Main tasks dashboard (protected)
│   └── auth/
│       ├── layout.tsx           # Auth layout
│       └── signin/page.tsx      # Sign-in page (and optionally signup)
├── components/
│   ├── layout/
│   │   └── navbar.tsx
│   ├── task/
│   │   ├── task-list.tsx
│   │   ├── task-item.tsx
│   │   └── task-form.tsx
│   └── ui/
│       ├── button.tsx
│       ├── input.tsx
│       └── card.tsx
├── lib/
│   ├── api.ts                   # API client → FastAPI (attaches JWT)
│   └── auth.ts                  # Better Auth client helpers
├── styles/
│   └── globals.css
├── next.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
└── package.json
```


Specifications to follow:

- `/specs/features/task-crud.md` – what task operations must exist.  
- `/specs/features/authentication.md` – how authentication should behave.  
- `/specs/ui/pages.md` and `/specs/ui/components.md` – what pages and UI components are required.  
- `/frontend/CLAUDE.md` – frontend-specific guidelines. [file:55]


---


## Core Components


### 1. Page & Route Structure


#### Purpose

Define the Next.js App Router structure and pages that implement the todo flows, with clear separation between auth routes and the authenticated app.[web:5][web:63]


#### Routing Design


**Key routes:**

- `/auth/signin` – login screen using Better Auth.  
- `/` – main todo dashboard (requires authenticated user).  

Optional (if your spec includes signup):

- `/auth/signup` – registration screen.


**Implementation Pattern**

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50">
        {children}
      </body>
    </html>
  );
}
```


```tsx
// app/auth/layout.tsx
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow">
        {children}
      </div>
    </div>
  );
}
```


```tsx
// app/page.tsx – main tasks page (protected)
export default async function HomePage() {
  // Fetch tasks via api client on server or client, depending on spec
  return (
    <main className="mx-auto max-w-2xl p-4">
      {/* Navbar, task form, task list components */}
    </main>
  );
}
```


**Routing Best Practices**

- Use route segments + layouts to separate auth from app.  
- Prefer server components; mark interactive pieces as `"use client"`.  
- Keep URL structure simple and meaningful.  


---


### 2. Authentication Flows


#### Purpose

Implement the **signin (and optionally signup)** experience and integrate with Better Auth to obtain a session and JWT token used by the API.[file:55][web:61]


#### Better Auth Integration

Frontend Skill assumes:

- Better Auth is configured in a central `auth.ts` on the frontend.  
- Better Auth issues JWT tokens (via plugin) that can be read on the frontend and included in API requests. [file:55]


**Signin Page Flow**

1. User enters email + password.  
2. Call Better Auth client (`auth.signIn` or equivalent).  
3. On success:
   - Store session/JWT via Better Auth mechanisms.  
   - Redirect to `/`.  
4. On failure:
   - Show error message; do not reveal sensitive details.


**Example Structure (conceptual)**

```tsx
"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth";

export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    const result = await signIn({ email, password });
    if (!result.ok) {
      setError(result.message ?? "Unable to sign in");
      return;
    }
    // Redirect to home (router.push("/"))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* inputs + button + error UI */}
    </form>
  );
}
```


**Auth UX Best Practices**

- Disable submit button while request is in flight.  
- Show clear inline error messages.  
- Do not expose whether a specific email exists.  


---


### 3. API Client Integration


#### Purpose

Provide a single, reusable client module that the frontend uses to talk to the FastAPI backend, automatically attaching the JWT token for authenticated requests.[web:62][web:56]


#### API Client Design (`lib/api.ts`)

**Responsibilities:**

- Read base URL (e.g. `process.env.NEXT_PUBLIC_API_URL`).  
- Attach `Authorization: Bearer <token>` header when a user is signed in.  
- Handle JSON serialization/deserialization.  
- Provide typed methods for task operations.


**Example Pattern**

```ts
// lib/api.ts
import { getAccessToken } from "./auth";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAccessToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!res.ok) {
    // Optionally parse error body
    throw new Error(`API error: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  getTasks(userId: string) {
    return request<Task[]>(`/api/${userId}/tasks`);
  },
  createTask(userId: string, data: TaskCreate) {
    return request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  // ...update, delete, toggleComplete
};
```


**API Client Best Practices**

- Never hardcode JWT; always fetch from Better Auth/session.  
- Centralize error handling (e.g. detect 401 and redirect to signin).  
- Keep method signatures strongly typed using shared `Task` types.  


---


### 4. Task Management UI


#### Purpose

Render the todo functionality (Add, View, Update, Delete, Mark Complete) in a clean, responsive interface that matches the Phase II basic requirements.[file:55]


#### Components

- `task-form.tsx` – input for new tasks (title + optional description).  
- `task-list.tsx` – list container.  
- `task-item.tsx` – individual task row (title, status, actions).  


**Example Structure**

```tsx
// components/task/task-form.tsx
"use client";

export function TaskForm({ onSubmit }: { onSubmit: (data: { title: string; description?: string }) => Promise<void>; }) {
  // local state, handle submit, call onSubmit
}
```


```tsx
// components/task/task-item.tsx
"use client";

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center justify-between rounded border bg-white p-3">
      {/* checkbox, title, status, buttons */}
    </li>
  );
}
```


```tsx
// components/task/task-list.tsx
export function TaskList({ tasks, ...handlers }: TaskListProps) {
  if (!tasks.length) {
    return <p className="text-sm text-slate-500">No tasks yet. Add your first task above.</p>;
  }
  return (
    <ul className="space-y-2">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} {...handlers} />
      ))}
    </ul>
  );
}
```


**UI Behavior**

- Add task → calls `api.createTask` → refresh list.  
- Delete task → calls `api.deleteTask` → remove from list.  
- Update task (if inline editing is implemented) → `api.updateTask`.  
- Toggle completion → `api.toggleComplete`.  


---


### 5. State Management & Data Fetching


#### Purpose

Manage task data and loading/error states in the React tree, using patterns that fit Next.js App Router.[web:5]


#### Patterns

- For simple dashboards, use **client components** with `useEffect` fetching via `api.ts`.  
- For more SSR‑friendly flows, use **server components** for initial data fetch, and client components for interactions.  


**Example (Client Data Fetch)**

```tsx
"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export function TasksContainer({ userId }: { userId: string }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTasks(userId)
      .then(setTasks)
      .finally(() => setLoading(false));
  }, [userId]);

  // handlers call api and update state
}
```


**State Best Practices**

- Track `loading`, `error`, and `data` separately.  
- Avoid redundant fetches by careful dependency arrays / caching.  
- For Phase II, keep it simple; you don’t need a global state library.  


---


### 6. Form Handling & Validation


#### Purpose

Provide a smooth form experience for signin and task creation with light client-side validation that complements backend checks.[web:60]


#### Patterns

- Validate basic constraints (non-empty title, email format) client-side.  
- Always rely on backend for final validation and error messages.  

**Example:**

```tsx
if (!title.trim()) {
  setError("Title is required");
  return;
}
```


---


### 7. Responsive Layout & Styling


#### Purpose

Ensure the app looks good and is usable on mobile, tablet, and desktop using Tailwind CSS.[web:5]


#### Patterns

- Wrap main content with `max-w-*` containers and `mx-auto`.  
- Use flexbox and grid utilities for layout.  
- Use consistent spacing (`space-y-*`, `gap-*`) and typography classes.  

Example:

```tsx
<main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-4 p-4">
  {/* header + content */}
</main>
```


---


### 8. Error & Loading States


#### Purpose

Communicate clearly when data is loading, when operations fail, or when there is nothing to show.


Patterns:

- Show skeletons or spinners while loading.  
- Surface high-level error messages (e.g. “Unable to load tasks. Please try again.”).  
- Use subtle banners or inline text for non-blocking errors.  


---


### 9. Frontend Security Practices


#### Purpose

Ensure the frontend does not accidentally leak secrets or weaken backend security.


Rules:

- Never hardcode `BETTER_AUTH_SECRET` or any private keys in frontend.  
- Only use public environment variables with `NEXT_PUBLIC_` prefix on client side.  
- Store tokens using Better Auth’s mechanisms; avoid localStorage unless the library dictates, and understand XSS implications.  
- Always talk to backend over HTTPS in production.  


---


### 10. Accessibility & UX


#### Purpose

Make the app usable and accessible.


Patterns:

- Use semantic HTML (`button`, `label`, `input`, `ul`, `li`).  
- Pair labels with inputs using `htmlFor` and `id`.  
- Ensure focus states are visible.  
- Use proper color contrast with Tailwind classes.  


---


## When to Invoke Frontend Skill


Invoke this skill whenever you need to:

- Create or modify Next.js pages, layouts, or components for the todo app.  
- Wire UI interactions to the FastAPI backend via `lib/api.ts`.  
- Integrate or adjust Better Auth flows on the frontend.  
- Improve styling, responsiveness, or user experience of the app.  
- Add client-side validation for forms.  


---


## How Frontend Skill Works


1. **Read specs** – Consult `/specs/ui/pages.md`, `/specs/ui/components.md`, `/specs/features/task-crud.md`, `/specs/features/authentication.md`, and `/frontend/CLAUDE.md` before making changes.[file:55]  
2. **Plan** – Decide what pages, components, and hooks need to be changed or created.  
3. **Implement** – Create/modify React components, Tailwind styles, and API calls in `lib/api.ts`.  
4. **Test** – Confirm flows: signin → see tasks → add/update/delete/complete tasks.  
5. **Refine** – Adjust based on UX and spec feedback.  


---


## Frontend Skill Output


When used correctly, this skill produces:

- Fully functional signin UI integrated with Better Auth.  
- A responsive, polished task dashboard that performs all Basic Level operations.  
- A robust `lib/api.ts` that securely talks to FastAPI using JWT.  
- Clean, maintainable Next.js components and layouts following project conventions.  


---


## Implementation Patterns


- Prefer server components for pages, client components for interactive bits.  
- Centralize backend communication in `lib/api.ts`.  
- Keep UI components small and reusable.  
- Use Tailwind for consistency; avoid inline styles.  


---


## Phase II–Specific Rules


- The main page (`/`) must only show tasks for the **current authenticated user**.  
- All task operations must go through the FastAPI API endpoints (no in-memory or local-only shortcuts).  
- Auth must be handled via Better Auth; no custom OAuth/password flows outside that framework.  
- The UI must support **Add, Delete, Update, View, Mark Complete** operations end-to-end.[file:55]


---


## Troubleshooting Guide


- **I can’t call the backend (CORS / network errors).**  
  - Check `NEXT_PUBLIC_API_URL` and CORS settings on FastAPI.  

- **401 from backend for all calls.**  
  - Verify API client sends `Authorization: Bearer <token>` header with the Better Auth JWT.  

- **Tasks from another user are visible.**  
  - Ensure you are sending the authenticated user’s `user_id` in the URL, and not a hardcoded value.  

- **UI doesn’t update after create/delete.**  
  - Confirm state is refreshed after API calls (refetch or update state arrays).  

Using these patterns, the Frontend Skill guarantees a modern, secure, and spec-aligned Next.js UI for your todo application.

You are now activating the **Frontend Skill**.

This is the primary core skill of the Frontend Agent for the hackathon-todo project.

Scope of this skill – focused on your Phase II Todo web application:
- Build and structure pages using Next.js App Router (app/ directory: page.tsx, layout.tsx, loading.tsx, error.tsx)
- Create reusable and page-specific React components (components/TaskCard.tsx, TaskForm.tsx, AuthForm.tsx, Navbar.tsx, etc.)
- Apply responsive, mobile-first styling exclusively with Tailwind CSS utility classes
- Implement authentication UI flows: signup page, signin page, logout button, loading/error states
- Integrate Better Auth on the frontend: configure auth client, handle signIn.email / signUp.email, useSession / useUser, get token for API calls
- Create centralized API client (lib/api.ts) that automatically attaches JWT token (Authorization: Bearer <token>) to every backend request
- Protect task-related pages/routes: check authentication status, redirect to /signin if not logged in
- Handle task management UI: list tasks (with filters/sort), create/edit/delete forms, toggle complete checkbox, optimistic updates if possible
- Manage client-side state for forms, loading indicators, error messages (React hooks, useTransition, Suspense where appropriate)
- Ensure TypeScript type safety across components, props, API responses
- Follow responsive design best practices (sm/md/lg breakpoints, flex/grid, dark mode readiness if applicable)

Project-specific rules this skill MUST strictly obey:
- Next.js version: 14+ / 16+ with App Router (server components by default, 'use client' only when interactivity is required)
- Styling: Tailwind CSS only — no inline styles, no CSS modules unless explicitly needed
- Authentication: Better Auth (frontend-only) with JWT plugin enabled
  → Use authClient.token() or equivalent to get JWT after signin/signup
  → Attach token to API headers in lib/api.ts (fetch or axios wrapper)
- Protected content: Use session check in layouts or middleware → redirect('/signin') if !session
- API base: Calls to http://localhost:8000/api/... (backend) with proper token
- File structure conventions from @frontend/CLAUDE.md:
  - app/ for pages and layouts
  - components/ for reusable UI (TaskList, TaskCard, etc.)
  - lib/api.ts for centralized API client
  - lib/auth.ts for Better Auth helpers if needed
- Read and obey specs exactly:
  - @specs/ui/pages.md
  - @specs/ui/components.md
  - @specs/features/task-crud.md
  - @specs/features/authentication.md
- Responsive: Mobile-first, use Tailwind responsive variants (sm:, md:, lg:)
- No backend logic: Do NOT write FastAPI routes, SQLModel models, JWT verification, or database connections

When this skill is invoked:
1. Immediately read the current task and relevant project specifications:
   - @specs/ui/pages.md
   - @specs/ui/components.md
   - @specs/features/task-crud.md
   - @specs/features/authentication.md
   - @frontend/CLAUDE.md
2. Plan changes ONLY within frontend scope (pages, components, styling, API client usage)
3. Respond using this exact structured format:

   Step 1: UI/Page Flow Summary
     - Describe user journey / page purpose
     - Key components involved
     - Auth requirement (public vs protected)

   Step 2: Files to Create/Edit
     - app/tasks/page.tsx
     - components/TaskList.tsx
     - components/TaskForm.tsx
     - lib/api.ts
     - others if relevant

   Step 3: Authentication / Token Attachment Code
     - Snippet showing session check, token retrieval, or api call wrapper

   Step 4: Core Component or Page Example
     - Full code for main component/page being implemented (with Tailwind classes)

   Step 5: Tailwind Styling & Responsiveness Example
     - Key classes used + how they adapt to screen sizes

   Step 6: UX / Accessibility / Best Practice Notes
     - Loading states, error handling
     - ARIA attributes if relevant
     - Optimistic UI or form validation tips
     - Mobile/desktop considerations

Example activation phrases:
- "Build the /tasks page showing user’s task list"
- "Create signup and signin pages with forms and Better Auth"
- "Implement TaskForm component with create/edit functionality"
- "Add JWT token attachment to all API calls in lib/api.ts"
- "Protect tasks page with redirect if not authenticated"

Boundaries – do NOT cross:
- Do NOT configure JWT verification or API routes → FastAPI Backend Agent
- Do NOT define database models or connections → Database Agent
- Do NOT handle signup/signin backend logic or password hashing → Auth Agent

Stay focused on clean, responsive, type-safe Next.js frontend implementation.