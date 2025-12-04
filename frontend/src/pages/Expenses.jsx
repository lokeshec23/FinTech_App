/**
 * Expenses Management Page
 */
import { useState, useEffect } from 'react';
import { expenseAPI } from '../services/api';
import { formatIndianCurrency, formatDate } from '../utils/formatters';
import { toast } from 'react-toastify';
import './Expenses.css';

const Expenses = () => {
    const [expenses, setExpenses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingExpense, setEditingExpense] = useState(null);
    const [formData, setFormData] = useState({
        category: 'Food & Dining',
        amount: '',
        description: '',
        date: new Date().toISOString().split('T')[0],
        payment_method: 'UPI'
    });

    const categories = [
        'Food & Dining', 'Transportation', 'Utilities', 'Entertainment',
        'Shopping', 'Healthcare', 'Education', 'Rent', 'Insurance',
        'Investments', 'Others'
    ];

    const paymentMethods = ['Cash', 'Card', 'UPI', 'Net Banking'];

    useEffect(() => {
        fetchExpenses();
    }, []);

    const fetchExpenses = async () => {
        try {
            const response = await expenseAPI.getAll();
            setExpenses(response.data);
        } catch (error) {
            toast.error('Failed to load expenses');
        }
        setLoading(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                ...formData,
                amount: parseFloat(formData.amount),
                date: new Date(formData.date).toISOString()
            };

            if (editingExpense) {
                await expenseAPI.update(editingExpense.id, data);
                toast.success('Expense updated successfully');
            } else {
                await expenseAPI.create(data);
                toast.success('Expense added successfully');
            }

            setShowModal(false);
            setEditingExpense(null);
            resetForm();
            fetchExpenses();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to save expense');
        }
    };

    const handleEdit = (expense) => {
        setEditingExpense(expense);
        setFormData({
            category: expense.category,
            amount: expense.amount.toString(),
            description: expense.description,
            date: new Date(expense.date).toISOString().split('T')[0],
            payment_method: expense.payment_method
        });
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this expense?')) return;

        try {
            await expenseAPI.delete(id);
            toast.success('Expense deleted successfully');
            fetchExpenses();
        } catch (error) {
            toast.error('Failed to delete expense');
        }
    };

    const resetForm = () => {
        setFormData({
            category: 'Food & Dining',
            amount: '',
            description: '',
            date: new Date().toISOString().split('T')[0],
            payment_method: 'UPI'
        });
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setEditingExpense(null);
        resetForm();
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loader"></div>
            </div>
        );
    }

    return (
        <div className="expenses-page">
            <div className="page-header">
                <div>
                    <h1>Expenses</h1>
                    <p className="text-muted">Track and manage your expenses</p>
                </div>
                <button onClick={() => setShowModal(true)} className="btn btn-primary">
                    + Add Expense
                </button>
            </div>

            <div className="expenses-grid">
                {expenses.length === 0 ? (
                    <div className="empty-state">
                        <p>No expenses found. Add your first expense to get started!</p>
                    </div>
                ) : (
                    expenses.map((expense) => (
                        <div key={expense.id} className="expense-card">
                            <div className="expense-header">
                                <span className="expense-category">{expense.category}</span>
                                <span className="expense-amount">{formatIndianCurrency(expense.amount)}</span>
                            </div>
                            <p className="expense-description">{expense.description}</p>
                            <div className="expense-footer">
                                <div className="expense-meta">
                                    <span className="expense-date">{formatDate(expense.date)}</span>
                                    <span className="expense-method">{expense.payment_method}</span>
                                </div>
                                <div className="expense-actions">
                                    <button onClick={() => handleEdit(expense)} className="btn-icon">
                                        ✏️
                                    </button>
                                    <button onClick={() => handleDelete(expense.id)} className="btn-icon btn-danger">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {showModal && (
                <div className="modal-overlay" onClick={handleCloseModal}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>{editingExpense ? 'Edit Expense' : 'Add Expense'}</h2>
                            <button onClick={handleCloseModal} className="modal-close">×</button>
                        </div>

                        <form onSubmit={handleSubmit} className="modal-form">
                            <div className="input-group">
                                <label className="input-label">Category</label>
                                <select
                                    className="input"
                                    value={formData.category}
                                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                                    required
                                >
                                    {categories.map(cat => (
                                        <option key={cat} value={cat}>{cat}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="input-group">
                                <label className="input-label">Amount (₹)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.amount}
                                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Description</label>
                                <textarea
                                    className="input"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="What did you spend on?"
                                    rows="3"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Date</label>
                                <input
                                    type="date"
                                    className="input"
                                    value={formData.date}
                                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Payment Method</label>
                                <select
                                    className="input"
                                    value={formData.payment_method}
                                    onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                                    required
                                >
                                    {paymentMethods.map(method => (
                                        <option key={method} value={method}>{method}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="modal-actions">
                                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingExpense ? 'Update' : 'Add'} Expense
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Expenses;
