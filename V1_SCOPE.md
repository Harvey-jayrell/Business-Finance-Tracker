# Business Finance Tracker — V1 Scope

**Goal of V1:** a deployed, documented backend API that a technical reviewer or client can try with a single URL.
**Not a goal of V1:** the mobile app, Investments, or any new features.

## Must work in the demo

- [x] `GET /api/health` reports app and database status
- [x] First-owner registration (`POST /api/auth/register`), closed after the first user
- [x] Login (`POST /api/auth/login`) returns a JWT carrying the user's role
- [x] Role enforcement: owner / manager / cashier get different access (shown via 401 / 403 / 404 responses)
- [ ] Categories: create (owner/manager) **and list** (check this exists; a client can't pick a `category_id` without it)
- [x] Expenses: create, list (role-scoped), edit (PATCH), soft-delete (cashier needs password re-confirm)
- [x] Owner can create employee accounts (`POST /api/users`) — verify this is built; otherwise move to Later or build it

## Definition of "deployed" for V1

- [x] `Dockerfile` builds and runs the backend locally
- [x] No secrets in the image or the repo (`DATABASE_URL`, `JWT_SECRET_KEY` come from environment variables)
- [ ] Supabase RLS decision made for the tables (understand it before the API is public)
- [ ] Test accounts and weak test passwords removed or replaced
- [ ] A few automated tests (pytest) covering login, role checks, and one expense flow
- [ ] GitHub Actions runs the tests on push
- [ ] Live on a public URL over HTTPS
- [ ] README with: what it is, architecture sketch, how to run it, example requests, and the role/permission table

## Later (do NOT start before V1 is live)

- Investments domain and the Manager → Owner approval workflow
- Dashboard endpoints
- Cashier password re-confirm on PATCH
- Remaining PATCH validation edge cases (title / date / category checks)
- User management beyond account creation (edit, deactivate)
- React Native mobile app
- Deprecation cleanup (`Query.get`, `datetime.utcnow`)
- Extra filters and search on expenses