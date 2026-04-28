import Layout from '../components/Layout';

export default function DashboardPage() {
  return (
    <Layout>
      <section className="grid gap-4 md:grid-cols-2">
        <article className="bg-white rounded shadow p-4">
          <h2 className="text-xl font-semibold">Inventory Intelligence</h2>
          <p>Track stock levels, thresholds, and expiry in one place.</p>
        </article>
        <article className="bg-white rounded shadow p-4">
          <h2 className="text-xl font-semibold">Vendor Workflow</h2>
          <p>Manage suppliers and purchase order lifecycle at scale.</p>
        </article>
      </section>
    </Layout>
  );
}
