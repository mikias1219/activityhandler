(function() {
  if (typeof lifeosRedirectLogin === 'function' && lifeosRedirectLogin()) return;

  var taskForm = document.getElementById('task-form');
  var taskFormEl = document.getElementById('task-form-el');
  var taskId = document.getElementById('task-id');
  var taskTitle = document.getElementById('task-title');
  var taskDue = document.getElementById('task-due');
  var taskPriority = document.getElementById('task-priority');
  var taskNotes = document.getElementById('task-notes');
  var tasksList = document.getElementById('tasks-list');
  var formTitle = document.getElementById('form-title');
  var isToday = (window.location.search || '').indexOf('view=today') >= 0;
  var listPath = isToday ? '/tasks/today/' : '/tasks/';

  function loadTasks() {
    lifeos.get(listPath).then(function(r) { return r.json(); }).then(function(data) {
      var items = data.results || (Array.isArray(data) ? data : []);
      if (items.length === 0) {
        tasksList.innerHTML = '<p class="p-6 text-slate-500 dark:text-slate-400">No tasks.</p>';
        return;
      }
      tasksList.innerHTML = items.map(function(t) {
        var due = t.due_date ? t.due_date : '';
        var priorityLabel = (t.priority || '').replace(/_/g, ' ');
        var status = t.status || 'todo';
        return '<div class="p-4 flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-700 last:border-0" data-id="' + t.id + '">' +
          '<div class="flex-1 min-w-0">' +
          '<span class="font-medium ' + (status === 'done' ? 'line-through text-slate-500' : '') + '">' + (t.title || '') + '</span>' +
          (due ? '<span class="text-sm text-slate-500 dark:text-slate-400 ml-2">' + due + '</span>') + '' +
          (priorityLabel ? '<span class="text-xs px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-600 ml-2">' + priorityLabel + '</span>') + '' +
          '</div>' +
          '<div class="flex gap-2">' +
          '<button type="button" class="task-edit px-2 py-1 rounded bg-slate-200 dark:bg-slate-600 text-sm">Edit</button>' +
          '<button type="button" class="task-delete px-2 py-1 rounded bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-300 text-sm">Delete</button>' +
          (status !== 'done' ? '<button type="button" class="task-done px-2 py-1 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 text-sm">Done</button>' : '') +
          '</div></div>';
      }).join('');
      tasksList.querySelectorAll('.task-edit').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          lifeos.get('/tasks/' + id + '/').then(function(r) { return r.json(); }).then(function(t) {
            taskId.value = t.id;
            taskTitle.value = t.title || '';
            taskDue.value = t.due_date || '';
            taskPriority.value = t.priority || 'not_urgent_not_important';
            taskNotes.value = t.notes || '';
            formTitle.textContent = 'Edit task';
            taskForm.classList.remove('hidden');
          });
        };
      });
      tasksList.querySelectorAll('.task-delete').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          if (confirm('Delete this task?')) {
            lifeos.delete('/tasks/' + id + '/').then(function() { loadTasks(); });
          }
        };
      });
      tasksList.querySelectorAll('.task-done').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          lifeos.patch('/tasks/' + id + '/', { status: 'done' }).then(function() { loadTasks(); });
        };
      });
    }).catch(function() {
      tasksList.innerHTML = '<p class="p-6 text-red-500">Failed to load tasks.</p>';
    });
  }

  document.getElementById('btn-new-task').onclick = function() {
    taskId.value = '';
    taskTitle.value = '';
    taskDue.value = new Date().toISOString().slice(0, 10);
    taskPriority.value = 'not_urgent_not_important';
    taskNotes.value = '';
    formTitle.textContent = 'New task';
    taskForm.classList.remove('hidden');
  };

  document.getElementById('btn-cancel-task').onclick = function() {
    taskForm.classList.add('hidden');
  };

  taskFormEl.onsubmit = function(e) {
    e.preventDefault();
    var id = taskId.value.trim();
    var payload = {
      title: taskTitle.value.trim(),
      due_date: taskDue.value || null,
      priority: taskPriority.value,
      notes: taskNotes.value.trim() || null
    };
    var p = id ? lifeos.patch('/tasks/' + id + '/', payload) : lifeos.post('/tasks/', payload);
    p.then(function() {
      taskForm.classList.add('hidden');
      loadTasks();
    }).catch(function(err) {
      alert('Failed to save task.');
    });
  };

  loadTasks();
})();
