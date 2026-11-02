import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from '@/context/AuthContext'
import { MainLayout } from '@/components/layout'
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { LoginPage, DashboardPage, InventoryPage, SalesPage, CustomersPage, EmployeesPage, CategoriesPage, PurchasesPage, SuppliersPage, ReportsPage } from '@/pages'

function App() {
  return <BrowserRouter><AuthProvider><Toaster position="top-right" toastOptions={{ duration: 3000, style: { background: '#fff', color: '#333' }, success: { iconTheme: { primary: '#10b981', secondary: '#fff' } }, error: { iconTheme: { primary: '#ef4444', secondary: '#fff' } } }} /><Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
      <Route index element={<Navigate to="/dashboard" replace />} />
      <Route path="dashboard" element={<DashboardPage />} />
      <Route path="inventory" element={<InventoryPage />} />
      <Route path="inventory/categories" element={<CategoriesPage />} />
      <Route path="inventory/movements" element={<InventoryPage />} />
      <Route path="inventory/adjustments" element={<InventoryPage />} />
      <Route path="sales" element={<SalesPage />} />
      <Route path="sales/new" element={<SalesPage />} />
      <Route path="sales/quotes" element={<SalesPage />} />
      <Route path="sales/receivables" element={<SalesPage />} />
      <Route path="purchases" element={<PurchasesPage />} />
      <Route path="purchases/new" element={<PurchasesPage />} />
      <Route path="purchases/suppliers" element={<SuppliersPage />} />
      <Route path="purchases/payables" element={<PurchasesPage />} />
      <Route path="customers" element={<CustomersPage />} />
      <Route path="employees" element={<EmployeesPage />} />
      <Route path="employees/sellers" element={<EmployeesPage />} />
      <Route path="employees/warehouse" element={<EmployeesPage />} />
      <Route path="reports" element={<ReportsPage />} />
      <Route path="reports/sales" element={<ReportsPage />} />
      <Route path="reports/inventory" element={<ReportsPage />} />
      <Route path="reports/profitability" element={<ReportsPage />} />
    </Route>
    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes></AuthProvider></BrowserRouter>
}

export default App
