export const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);

export function validateProductForm(form) {
  if (!form.name || form.name.length < 2) return 'Product name must be at least 2 chars';
  if (!form.sku) return 'SKU is required';
  if (Number(form.stock) < 0) return 'Stock cannot be negative';
  if (Number(form.price) <= 0) return 'Price must be positive';
  if (Number(form.threshold) < 0) return 'Threshold cannot be negative';
  return '';
}
