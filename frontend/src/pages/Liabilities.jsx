/**
 * Liabilities Management Page
 */
import { useState, useEffect } from 'react';
import { liabilityAPI } from '../services/api';
import { formatIndianCurrency, formatDate } from '../utils/formatters';
import { toast } from 'react-toastify';
import '../pages/Expenses.css';

const Liabilities = () => {
    const [liabilities, setLiabilities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingLiability, setEditingLiability] = useState(null);
    const [formData, setFormData] = useState({
        liability_type: 'Personal Loan',
        name: '',
        amount: '',
        interest_rate: '',
        due_date: ''
    });

    const liabilityTypes = [
        'Personal Loan', 'Home Loan', 'Car Loan', 'Credit Card',
        'Education Loan', 'Business Loan', 'Others'
    ];

    useEffect(() => {
        fetchLiabilities();
    }, []);

    const fetchLiabilities = async () => {
        try {
            const response = await liabilityAPI.getAll();
            setLiabilities(response.data);
        } catch (error) {
            toast.error('Failed to load liabilities');
        }
        setLoading(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                liability_type: formData.liability_type,
                name: formData.name,
                amount: parseFloat(formData.amount),
                interest_rate: formData.interest_rate ? parseFloat(formData.interest_rate) : null,
                due_date: formData.due_date || null
            };

            if (editingLiability) {
                await liabilityAPI.update(editingLiability.id, data);
                toast.success('Liability updated successfully');
            } else {
                await liabilityAPI.create(data);
                toast.success('Liability added successfully');
            }

            setShowModal(false);
            setEditingLiability(null);
            resetForm();
            fetchLiabilities();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to save liability');
        }
    };

    const handleEdit = (liability) => {
        setEditingLiability(liability);
        setFormData({
            liability_type: liability.liability_type,
            name: liability.name,
            amount: liability.amount.toString(),
            interest_rate: liability.interest_rate?.toString() || '',
            due_date: liability.due_date || ''
        });
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this liability?')) return;

        try {
            await liabilityAPI.delete(id);
            toast.success('Liability deleted successfully');
            fetchLiabilities();
        } catch (error) {
            toast.error('Failed to delete liability');
        }
    };

    const resetForm = () => {
        setFormData({
            liability_type: 'Personal Loan',
            name: '',
            amount: '',
            interest_rate: '',
            due_date: ''
        });
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setEditingLiability(null);
        resetForm();
    };

    if (loading) {
        return <div className="loading-container"><div className="loader"></div></div>;
    }

    return (
        <div className="expenses-page">
            <div className="page-header">
                <div>
                    <h1>Liabilities</h1>
                    <p className="text-muted">Track your debts and loans</p>
                </div>
                <button onClick={() => setShowModal(true)} className="btn btn-primary">
                    + Add Liability
                </button>
            </div>

            <div className="expenses-grid">
                {liabilities.length === 0 ? (
                    <div className="empty-state">
                        <p>No liabilities found. Add your first liability to track debts!</p>
                    </div>
                ) : (
                    liabilities.map((liability) => (
                        <div key={liability.id} className="expense-card">
                            <div className="expense-header">
                                <span className="expense-category">{liability.liability_type}</span>
                                <span className="expense-amount" style={{ color: 'var(--danger-color)' }}>
                                    {formatIndianCurrency(liability.amount)}
                                </span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{liability.name}</h3>
                            <div className="expense-footer">
                                <div className="expense-meta">
                                    <span className="expense-method">
                                        Status: {liability.status}
                                    </span>
                                    {liability.interest_rate && (
                                        <span>Rate: {liability.interest_rate}%</span>
                                    )}
                                    {liability.due_date && (
                                        <span>Due: {formatDate(liability.due_date)}</span>
                                    )}
                                </div>
                                <div className="expense-actions">
                                    <button onClick={() => handleEdit(liability)} className="btn-icon">✏️</button>
                                    <button onClick={() => handleDelete(liability.id)} className="btn-icon btn-danger">🗑️</button>
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
                            <h2>{editingLiability ? 'Edit Liability' : 'Add Liability'}</h2>
                            <button onClick={handleCloseModal} className="modal-close">×</button>
                        </div>

                        <form onSubmit={handleSubmit} className="modal-form">
                            <div className="input-group">
                                <label className="input-label">Liability Type</label>
                                <select
                                    className="input"
                                    value={formData.liability_type}
                                    onChange={(e) => setFormData({ ...formData, liability_type: e.target.value })}
                                    required
                                >
                                    {liabilityTypes.map(type => (
                                        <option key={type} value={type}>{type}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="input-group">
                                <label className="input-label">Name</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    placeholder="e.g., HDFC Home Loan"
                                    required
                                />
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
                                <label className="input-label">Interest Rate (%) - Optional</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.interest_rate}
                                    onChange={(e) => setFormData({ ...formData, interest_rate: e.target.value })}
                                    placeholder="e.g., 8.5"
                                    step="0.01"
                                    min="0"
                                    max="100"
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Due Date - Optional</label>
                                <input
                                    type="date"
                                    className="input"
                                    value={formData.due_date}
                                    onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                                />
                            </div>

                            <div className="modal-actions">
                                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingLiability ? 'Update' : 'Add'} Liability
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Liabilities;
