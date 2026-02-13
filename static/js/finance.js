if (typeof lifeosRedirectLogin === 'function' && lifeosRedirectLogin()) void 0;
else (function() {
  var catSelect = document.getElementById('exp-cat');
  var reportBox = document.getElementById('report-box');
  var expensesList = document.getElementById('expenses-list');
  var categoriesListEl = document.getElementById('categories-list');

  function loadCategories() {
    lifeos.get('/expense-categories/').then(function(r) { return r.json(); }).then(function(data) {
      var items = data.results || [];
      categoriesListEl.innerHTML = items.map(function(c) {
        return '<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-slate-200 dark:bg-slate-700 text-sm" data-id="' + c.id + '">' +
          (c.name || '') +
          ' <button type="button" class="cat-delete text-red-600 hover:underline text-xs">Delete</button></span>';
      }).join('');
      categoriesListEl.querySelectorAll('.cat-delete').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          if (confirm('Delete this category? Expenses in it will need another category.')) {
            lifeos.delete('/expense-categories/' + id + '/').then(function() { loadCategories(); loadExpenses(); });
          }
        };
      });
      var catOpts = '<option value="">Select category</option>' + items.map(function(c) { return '<option value="' + c.id + '">' + (c.name || '') + '</option>'; }).join('');
      catSelect.innerHTML = catOpts;
      var budgetCat = document.getElementById('budget-cat');
      if (budgetCat) budgetCat.innerHTML = catOpts;
    });
  }

  document.getElementById('cat-form').onsubmit = function(e) {
    e.preventDefault();
    var name = document.getElementById('cat-name').value.trim();
    if (!name) return;
    lifeos.post('/expense-categories/', { name: name }).then(function() { document.getElementById('cat-name').value = ''; loadCategories(); });
  };

  document.getElementById('expense-form').onsubmit = function(e) {
    e.preventDefault();
    var catId = document.getElementById('exp-cat').value;
    var amount = document.getElementById('exp-amount').value;
    var date = document.getElementById('exp-date').value || new Date().toISOString().slice(0, 10);
    var note = document.getElementById('exp-note').value.trim();
    if (!catId || !amount) return;
    lifeos.post('/expenses/', { category: parseInt(catId, 10), amount: amount, currency: 'USD', expense_date: date, note: note }).then(function() {
      document.getElementById('exp-amount').value = '';
      document.getElementById('exp-note').value = '';
      loadExpenses();
    });
  };

  document.getElementById('btn-report').onclick = function() {
    var month = document.getElementById('report-month').value;
    if (!month) { reportBox.innerHTML = '<p class="text-slate-500">Select a month.</p>'; return; }
    lifeos.get('/expenses/report/?month=' + month).then(function(r) { return r.json(); }).then(function(data) {
      var total = data.total != null ? data.total : 0;
      var byCat = (data.by_category || []).map(function(c) { return (c.category__name || 'Other') + ': ' + c.total; }).join(', ');
      reportBox.innerHTML = '<p class="font-semibold">' + data.month + '</p><p class="text-2xl font-bold text-emerald-600 mt-2">Total: ' + total + ' USD</p><p class="text-sm text-slate-500 mt-2">' + (byCat || 'No expenses') + '</p>';
    });
  };

  function loadExpenses() {
    lifeos.get('/expenses/').then(function(r) { return r.json(); }).then(function(data) {
      var items = (data.results || []).slice(0, 30);
      if (items.length === 0) { expensesList.innerHTML = '<p class="p-6 text-slate-500 dark:text-slate-400">No expenses.</p>'; return; }
      expensesList.innerHTML = items.map(function(e) {
        var catName = (e.category && e.category.name) ? e.category.name : (e.category_name || '');
        return '<div class="p-4 flex justify-between items-center border-b border-slate-200 dark:border-slate-700 last:border-0" data-id="' + e.id + '">' +
          '<span class="text-slate-700 dark:text-slate-300">' + (e.expense_date || '') + ' ' + (catName ? '[' + catName + '] ' : '') + (e.note || '') + '</span>' +
          '<span class="font-medium">' + e.amount + ' ' + (e.currency || 'USD') + '</span>' +
          '<div class="flex gap-2"><button type="button" class="exp-delete px-2 py-1 rounded bg-red-100 dark:bg-red-900/40 text-red-700 text-sm">Delete</button></div></div>';
      }).join('');
      expensesList.querySelectorAll('.exp-delete').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          if (confirm('Delete this expense?')) {
            lifeos.delete('/expenses/' + id + '/').then(function() { loadExpenses(); });
          }
        };
      });
    }).catch(function() { expensesList.innerHTML = '<p class="p-6 text-red-500">Failed to load.</p>'; });
  }

  document.getElementById('exp-date').value = new Date().toISOString().slice(0, 10);
  var m = new Date();
  document.getElementById('report-month').value = m.getFullYear() + '-' + String(m.getMonth() + 1).padStart(2, '0');
  document.getElementById('budget-month').value = m.getFullYear() + '-' + String(m.getMonth() + 1).padStart(2, '0');

  function loadBudgets() {
    lifeos.get('/budgets/').then(function(r) { return r.json(); }).then(function(data) {
      var items = data.results || [];
      var listEl = document.getElementById('budgets-list');
      if (items.length === 0) { listEl.innerHTML = '<p class="text-slate-500 dark:text-slate-400 text-sm">No budgets. Add one above.</p>'; return; }
      listEl.innerHTML = items.map(function(b) {
        var catName = (b.category && b.category.name) ? b.category.name : ('Category #' + (b.category || ''));
        return '<div class="p-3 flex justify-between items-center border border-slate-200 dark:border-slate-700 rounded-lg mb-2" data-id="' + b.id + '">' +
          '<span class="text-slate-700 dark:text-slate-300">' + (b.month || '') + ' ' + catName + ' — ' + b.amount + ' ' + (b.currency || 'USD') + '</span>' +
          '<button type="button" class="budget-delete px-2 py-1 rounded bg-red-100 dark:bg-red-900/40 text-red-700 text-sm">Delete</button></div>';
      }).join('');
      listEl.querySelectorAll('.budget-delete').forEach(function(btn) {
        btn.onclick = function() {
          var id = btn.closest('[data-id]').getAttribute('data-id');
          if (confirm('Delete this budget?')) { lifeos.delete('/budgets/' + id + '/').then(function() { loadBudgets(); }); }
        };
      });
    });
  }

  document.getElementById('budget-form').onsubmit = function(e) {
    e.preventDefault();
    var catId = document.getElementById('budget-cat').value;
    var month = document.getElementById('budget-month').value;
    var amount = document.getElementById('budget-amount').value;
    if (!catId || !month || !amount) return;
    lifeos.post('/budgets/', { category: parseInt(catId, 10), month: month, amount: amount, currency: 'USD' }).then(function() {
      document.getElementById('budget-amount').value = '';
      loadBudgets();
    }).catch(function() { alert('Failed to add budget.'); });
  };

  loadCategories();
  loadExpenses();
  loadBudgets();
})();
