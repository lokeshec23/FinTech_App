/**
 * EMI Management Page
 */
import { useState, useEffect } from 'react';
import { emiAPI } from '../services/api';
import { formatIndianCurrency, formatDate } from '../utils/formatters';
import { toast } from 'react-toastify';
import '../pages/Expenses.css';

const EMIs = () => {
    const [emis, setEmis] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        lender_name: '',
        principal_amount: '',
        interest_rate: '',
        tenure_months: '',
        start_date: new Date().toISOString().split('T')[0],
        description: ''
    });

    useEffect(() => {
        fetchEMIs();
    }, []);

    const fetchEMIs = async () => {
        try {
            const response = await emiAPI.getAll();
            setEmis(response.data);
        } catch (error) {
            toast.error('Failed to load EMIs');
        }
        setLoading(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                ...formData,
                principal_amount: parseFloat(formData.principal_amount),
                interest_rate: parseFloat(formData.interest_rate),
                tenure_months: parseInt(formData.tenure_months),
                start_date: new Date(formData.start_date).toISOString()
            };

            await emiAPI.create(data);
            toast.success('EMI added successfully');
            setShowModal(false);
            resetForm();
            fetchEMIs();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to save EMI');
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this EMI?')) return;

        try {
            await emiAPI.delete(id);
            toast.success('EMI deleted successfully');
            fetchEMIs();
        } catch (error) {
            toast.error('Failed to delete EMI');
        }
    };

    const resetForm = () => {
        setFormData({
            lender_name: '',
            principal_amount: '',
            interest_rate: '',
            tenure_months: '',
            start_date: new Date().toISOString().split('T')[0],
            description: ''
        });
    };

    const handleCloseModal = () => {
        setShowModal(false);
        resetForm();
    };

    if (loading) {
        return <div className="loading-container"><div className="loader"></div></div>;
    }

    return (
        <div className="expenses-page">
            <div className="page-header">
                <div>
                    <h1>EMI Management</h1>
                    <p className="text-muted">Track your loans and EMI payments</p>
                </div>
                <button onClick={() => setShowModal(true)} className="btn btn-primary">
                    + Add EMI
                </button>
            </div>

            <div className="expenses-grid">
                {emis.length === 0 ? (
                    <div className="empty-state">
                        <p>No EMIs found. Add your first EMI/loan to get started!</p>
                    </div>
                ) : (
                    emis.map((emi) => (
                        <div key={emi.id} className="expense-card">
                            <div className="expense-header">
                                <span className="expense-category">{emi.lender_name}</span>
                                <span className="expense-amount">{formatIndianCurrency(emi.monthly_emi)}</span>
                            </div>
                            <p className="expense-description">{emi.description || 'No description'}</p>
                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                                    <span>Principal:</span>
                                    <strong>{formatIndianCurrency(emi.principal_amount)}</strong>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                                    <span>Interest Rate:</span>
                                    <strong>{emi.interest_rate}% p.a.</strong>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                                    <span>Tenure:</span>
                                    <strong>{emi.tenure_months} months</strong>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                                    <span>Remaining:</span>
                                    <strong>{emi.remaining_tenure} months</strong>
                                </div>
                            </div>
                            <div className="expense-footer">
                                <div className="expense-meta">
                                    <span className="expense-method">{emi.status}</span>
                                    <span>Start: {formatDate(emi.start_date)}</span>
                                </div>
                                <div className="expense-actions">
                                    <button onClick={() => handleDelete(emi.id)} className="btn-icon btn-danger">🗑️</button>
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
                            <h2>Add EMI / Loan</h2>
                            <button onClick={handleCloseModal} className="modal-close">×</button>
                        </div>

                        <form onSubmit={handleSubmit} className="modal-form">
                            <div className="input-group">
                                <label className="input-label">Lender Name</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.lender_name}
                                    onChange={(e) => setFormData({ ...formData, lender_name: e.target.value })}
                                    placeholder="e.g., HDFC Bank"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Principal Amount (₹)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.principal_amount}
                                    onChange={(e) => setFormData({ ...formData, principal_amount: e.target.value })}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Interest Rate (% per annum)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.interest_rate}
                                    onChange={(e) => setFormData({ ...formData, interest_rate: e.target.value })}
                                    placeholder="e.g., 8.5"
                                    step="0.01"
                                    min="0"
                                    max="100"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Tenure (months)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.tenure_months}
                                    onChange={(e) => setFormData({ ...formData, tenure_months: e.target.value })}
                                    placeholder="e.g., 60"
                                    min="1"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Start Date</label>
                                <input
                                    type="date"
                                    className="input"
                                    value={formData.start_date}
                                    onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Description - Optional</label>
                                <textarea
                                    className="input"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="Purpose of loan..."
                                    rows="3"
                                />
                            </div>

                            <div className="modal-actions">
                                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    Calculate & Add EMI
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EMIs;
