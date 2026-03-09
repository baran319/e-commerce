/* Cart AJAX quantity update */
function updateQty(itemId, delta) {
  const input = document.getElementById('qty' + itemId);
  const max = parseInt(input.max) || 999;
  let val = parseInt(input.value) + delta;
  val = Math.max(1, Math.min(val, max));
  input.value = val;
  submitUpdate(itemId);
}

function submitUpdate(itemId) {
  const form = document.getElementById('updateForm' + itemId);
  const input = document.getElementById('qty' + itemId);
  const csrfToken = form.querySelector('[name="csrf_token"]').value;
  const qty = parseInt(input.value);

  const data = new FormData();
  data.append('csrf_token', csrfToken);
  data.append('item_id', itemId);
  data.append('quantity', qty);

  fetch('/cart/update', {
    method: 'POST',
    body: data,
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(r => r.json())
  .then(res => {
    if (res.success) {
      const priceEl = document.getElementById('itemPrice' + itemId);
      if (priceEl) priceEl.textContent = res.item_subtotal.toFixed(2) + '₺';
      const totalEl = document.getElementById('cartTotal');
      if (totalEl) totalEl.textContent = res.cart_total.toFixed(2) + '₺';
      const badge = document.getElementById('cartBadge');
      if (badge) badge.textContent = res.cart_count;
    }
  })
  .catch(err => console.error('Cart update failed', err));
}
