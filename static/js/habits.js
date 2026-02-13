(function() {
  if (typeof lifeosRedirectLogin === 'function' && lifeosRedirectLogin()) return;

  var habitForm = document.getElementById('habit-form');
  var habitFormEl = document.getElementById('habit-form-el');
  var habitId = document.getElementById('habit-id');
  var habitName = document.getElementById('habit-name');
  var habitFreq = document.getElementById('habit-freq');
  var habitCount = document.getElementById('habit-count');
  var habitsList = document.getElementById('habits-list');

  function loadHabits() {
    lifeos.get('/habits/').then(function(r) { return r.json(); }).then(function(data) {
      var items = data.results || (Array.isArray(data) ? data : []);
      if (items.length === 0) {
        habitsList.innerHTML = '<p class="p-6 text-slate-500 dark:text-slate-400">No habits. Add one to start tracking.</p>';
        return;
      }
      habitsList.innerHTML = items.map(function(h) {
        return '<div class="habit-card p-4 mb-4 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700" data-id="' + h.id + '">' +
          '<div class="flex justify-between items-start gap-2">' +
          '<div><span class="font-semibold text-slate-800 dark:text-slate-100">' + (h.name || '') + '</span>' +
          '<span class="text-sm text-slate-500 dark:text-slate-400 ml-2">' + (h.target_frequency || 'daily') + '</span>' +
          '<span class="streak-badge text-sm ml-2 text-emerald-600 dark:text-emerald-400"></span></div>' +
          '<div class="flex gap-2">' +
          '<button type="button" class="habit-edit px-2 py-1 rounded bg-slate-200 dark:bg-slate-600 text-sm">Edit</button>' +
          '<button type="button" class="habit-delete px-2 py-1 rounded bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-300 text-sm">Delete</button>' +
          '</div></div>' +
          '<div class="habit-check-ins mt-2 text-sm text-slate-600 dark:text-slate-300"></div>' +
          '<div class="mt-2"><button type="button" class="habit-check-in-btn px-2 py-1 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 text-sm">Check in today</button></div>' +
          '</div>';
      }).join('');
      items.forEach(function(h, idx) {
        var card = habitsList.querySelectorAll('.habit-card')[idx];
        if (!card) return;
        card.querySelector('.habit-edit').onclick = function() {
          habitId.value = h.id;
          habitName.value = h.name || '';
          habitFreq.value = h.target_frequency || 'daily';
          habitCount.value = h.target_count != null ? h.target_count : 1;
          habitForm.classList.remove('hidden');
        };
        card.querySelector('.habit-delete').onclick = function() {
          if (confirm('Delete habit "' + (h.name || '') + '"?')) {
            lifeos.delete('/habits/' + h.id + '/').then(function() { loadHabits(); });
          }
        };
        card.querySelector('.habit-check-in-btn').onclick = function() {
          var today = new Date().toISOString().slice(0, 10);
          lifeos.post('/habits/' + h.id + '/check-ins/', { check_date: today, completed: true }).then(function() {
            loadCheckIns(h.id, card);
            loadStreak(h.id, card);
          });
        };
        loadCheckIns(h.id, card);
        loadStreak(h.id, card);
      });
    }).catch(function() {
      habitsList.innerHTML = '<p class="p-6 text-red-500">Failed to load habits.</p>';
    });
  }

  function loadCheckIns(habitPk, card) {
    var container = card.querySelector('.habit-check-ins');
    lifeos.get('/habits/' + habitPk + '/check-ins/').then(function(r) { return r.json(); }).then(function(data) {
      var items = (data.results || (Array.isArray(data) ? data : [])).slice(0, 7);
      container.innerHTML = items.length ? 'Recent: ' + items.map(function(c) {
        return '<span class="inline-block px-2 py-0.5 rounded ' + (c.completed ? 'bg-emerald-100 dark:bg-emerald-900/40' : 'bg-slate-200 dark:bg-slate-600') + '">' + (c.check_date || '') + '</span>';
      }).join(' ') : 'No check-ins yet.';
    });
  }

  function loadStreak(habitPk, card) {
    var badge = card.querySelector('.streak-badge');
    lifeos.get('/habits/' + habitPk + '/streak/').then(function(r) { return r.json(); }).then(function(data) {
      var n = data.current_streak != null ? data.current_streak : 0;
      badge.textContent = n ? '🔥 ' + n + ' day streak' : '';
    }).catch(function() { badge.textContent = ''; });
  }

  document.getElementById('btn-new-habit').onclick = function() {
    habitId.value = '';
    habitName.value = '';
    habitFreq.value = 'daily';
    habitCount.value = 1;
    habitForm.classList.remove('hidden');
  };

  document.getElementById('btn-cancel-habit').onclick = function() {
    habitForm.classList.add('hidden');
  };

  habitFormEl.onsubmit = function(e) {
    e.preventDefault();
    var id = habitId.value.trim();
    var payload = {
      name: habitName.value.trim(),
      target_frequency: habitFreq.value,
      target_count: parseInt(habitCount.value, 10) || 1
    };
    var p = id ? lifeos.patch('/habits/' + id + '/', payload) : lifeos.post('/habits/', payload);
    p.then(function() {
      habitForm.classList.add('hidden');
      loadHabits();
    }).catch(function() { alert('Failed to save habit.'); });
  };

  loadHabits();
})();
