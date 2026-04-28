import ApiState from '../components/ApiState';
import Layout from '../components/Layout';
import ProductForm from '../components/ProductForm';
import { useProducts } from '../hooks/useProducts';

export default function ProductsPage() {
  const { products, loading, error, add } = useProducts();

  return (
    <Layout>
      <div className="space-y-4">
        <ProductForm onSubmit={add} />
        <ApiState loading={loading} error={error}>
          <div className="overflow-x-auto bg-white rounded shadow">
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="text-left p-2">Name</th>
                  <th className="text-left p-2">SKU</th>
                  <th className="text-left p-2">Stock</th>
                  <th className="text-left p-2">Price</th>
                  <th className="text-left p-2">Threshold</th>
                </tr>
              </thead>
              <tbody>
                {products.map((item) => (
                  <tr key={item.id} className="border-t">
                    <td className="p-2">{item.name}</td>
                    <td className="p-2">{item.sku}</td>
                    <td className="p-2">{item.stock}</td>
                    <td className="p-2">${item.price}</td>
                    <td className="p-2">{item.threshold}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </ApiState>
      </div>
    </Layout>
  );
}
