/**
 * Bank Accounts Management Page
 */
import { useState, useEffect } from 'react';
import { bankAccountAPI } from '../services/api';
import { formatIndianCurrency } from '../utils/formatters';
import { toast } from 'react-toastify';
import '../pages/Expenses.css'; // Reuse expense page styles

const BankAccounts = () => {
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingAccount, setEditingAccount] = useState(null);
    const [formData, setFormData] = useState({
        bank_name: '',
        account_number: '',
        account_type: 'Savings',
        balance: '',
        currency: 'INR'
    });

    const accountTypes = ['Savings', 'Current', 'Salary'];

    useEffect(() => {
        fetchAccounts();
    }, []);

    const fetchAccounts = async () => {
        try {
            const response = await bankAccountAPI.getAll();
            setAccounts(response.data);
        } catch (error) {
            toast.error('Failed to load bank accounts');
        }
        setLoading(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                ...formData,
                balance: parseFloat(formData.balance)
            };

            if (editingAccount) {
                await bankAccountAPI.update(editingAccount.id, data);
                toast.success('Account updated successfully');
            } else {
                await bankAccountAPI.create(data);
                toast.success('Account added successfully');
            }

            setShowModal(false);
            setEditingAccount(null);
            resetForm();
            fetchAccounts();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to save account');
        }
    };

    const handleEdit = (account) => {
        setEditingAccount(account);
        setFormData({
            bank_name: account.bank_name,
            account_number: account.account_number,
            account_type: account.account_type,
            balance: account.balance.toString(),
            currency: account.currency
        });
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this account?')) return;

        try {
            await bankAccountAPI.delete(id);
            toast.success('Account deleted successfully');
            fetchAccounts();
        } catch (error) {
            toast.error('Failed to delete account');
        }
    };

    const resetForm = () => {
        setFormData({
            bank_name: '',
            account_number: '',
            account_type: 'Savings',
            balance: '',
            currency: 'INR'
        });
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setEditingAccount(null);
        resetForm();
    };

    if (loading) {
        return <div className="loading-container"><div className="loader"></div></div>;
    }

    return (
        <div className="expenses-page">
            <div className="page-header">
                <div>
                    <h1>Bank Accounts</h1>
                    <p className="text-muted">Manage your bank accounts</p>
                </div>
                <button onClick={() => setShowModal(true)} className="btn btn-primary">
                    + Add Account
                </button>
            </div>

            <div className="expenses-grid">
                {accounts.length === 0 ? (
                    <div className="empty-state">
                        <p>No bank accounts found. Add your first account to get started!</p>
                    </div>
                ) : (
                    accounts.map((account) => (
                        <div key={account.id} className="expense-card">
                            <div className="expense-header">
                                <span className="expense-category">{account.account_type}</span>
                                <span className="expense-amount">{formatIndianCurrency(account.balance)}</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{account.bank_name}</h3>
                            <p className="expense-description">Account: ****{account.account_number.slice(-4)}</p>
                            <div className="expense-footer">
                                <div className="expense-meta">
                                    <span className="expense-method">{account.currency}</span>
                                </div>
                                <div className="expense-actions">
                                    <button onClick={() => handleEdit(account)} className="btn-icon">✏️</button>
                                    <button onClick={() => handleDelete(account.id)} className="btn-icon btn-danger">🗑️</button>
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
                            <h2>{editingAccount ? 'Edit Account' : 'Add Bank Account'}</h2>
                            <button onClick={handleCloseModal} className="modal-close">×</button>
                        </div>

                        <form onSubmit={handleSubmit} className="modal-form">
                            <div className="input-group">
                                <label className="input-label">Bank Name</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.bank_name}
                                    onChange={(e) => setFormData({ ...formData, bank_name: e.target.value })}
                                    placeholder="e.g., State Bank of India"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Account Number</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.account_number}
                                    onChange={(e) => setFormData({ ...formData, account_number: e.target.value })}
                                    placeholder="Account number"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Account Type</label>
                                <select
                                    className="input"
                                    value={formData.account_type}
                                    onChange={(e) => setFormData({ ...formData, account_type: e.target.value })}
                                    required
                                >
                                    {accountTypes.map(type => (
                                        <option key={type} value={type}>{type}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="input-group">
                                <label className="input-label">Balance (₹)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.balance}
                                    onChange={(e) => setFormData({ ...formData, balance: e.target.value })}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="modal-actions">
                                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingAccount ? 'Update' : 'Add'} Account
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BankAccounts;
