# LifeOS — Calendar Alignment

LifeOS is aligned with your **Professional Weekly Google Calendar** (see `/main.py` in the parent project) so tasks, habits, and reminders can work in sync with your existing routine.

## Your calendar setup (reference)

- **Calendar**: `mikiyasabate003@gmail.com`
- **Timezone**: `Africa/Addis_Ababa` (GMT+3)
- **Reminders**: 5–10 minutes before events
- **Structure**:
  - **Weekdays**: Morning exercise & spiritual → Prepare for job → Commute + reading → Job + certification (7:30–18:30) → Gym → Dinner → Professional reading (21:30–23:00)
  - **Saturday**: Exercise + spiritual → Skill development → Market → Arsenal match slot
  - **Sunday**: Spiritual → Wash + planning → Arsenal match → Family time

## How LifeOS aligns

1. **Daily planner (`/api/v1/tasks/today/`)**
   - Shows tasks due **today** in your timezone. Use this as your “today” list alongside your calendar blocks.

2. **Task due dates**
   - Set task `due_date` to match calendar days (e.g. “Review certification” on weekdays). LifeOS does not set time; your calendar holds the exact slots.

3. **Habits**
   - Align habits with calendar blocks (e.g. “Morning run” after 5:00 AM block, “Gym” after 18:30). Check in via `/api/v1/habits/{id}/check-ins/` when you complete the block.

4. **Reminders (Phase 2)**
   - Use **Automation → Reminders** (`/api/v1/automation/reminders/`) for one-off or recurring reminders. Optionally run a Celery beat task to send notifications at specific times (e.g. 5 minutes before a calendar block).

5. **AI “What should I do now?”**
   - `/api/v1/ai/what-to-do-now/` uses **today’s tasks** and **habits not yet checked in** to suggest the next focus. Use it between calendar blocks.

## Using the activityhandler repo

- **Repo**: [https://github.com/mikias1219/activityhandler](https://github.com/mikias1219/activityhandler)
- LifeOS (this project) can be pushed to **activityhandler** as the main app; the deploy workflow is set up for that repo.
- To push this code to activityhandler:
  ```bash
  git remote add activityhandler https://github.com/mikias1219/activityhandler.git
  git push activityhandler main
  ```
- Your existing **main.py** calendar script can stay in the same repo or a sibling folder; LifeOS does not replace it but complements it with tasks, habits, finance, and AI.

## Optional: Google Calendar sync (future)

A future **integrations** module could:
- Read events from your Google Calendar (same service account as `main.py`) and show “today’s events” in the LifeOS dashboard.
- Create LifeOS tasks from calendar events or the reverse (e.g. “Add today’s tasks to calendar”).

For now, using **due_date** and **today view** in LifeOS plus your existing calendar gives you alignment without code changes.
