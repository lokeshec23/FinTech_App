/**
 * Indian currency and number formatting utilities
 */

/**
 * Format amount in Indian currency format (₹ with lakhs/crores)
 * Example: 1234567.89 -> ₹12,34,567.89
 */
export const formatIndianCurrency = (amount) => {
    if (amount === null || amount === undefined) return '₹0.00';

    const isNegative = amount < 0;
    const absAmount = Math.abs(amount);

    // Split into integer and decimal parts
    const [integerPart, decimalPart = '00'] = absAmount.toFixed(2).split('.');

    // Indian number system formatting
    let formatted;
    if (integerPart.length <= 3) {
        formatted = integerPart;
    } else {
        // Last 3 digits
        const lastThree = integerPart.slice(-3);
        const remaining = integerPart.slice(0, -3);

        // Add commas every 2 digits from right to left
        formatted = remaining.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + lastThree;
    }

    return `${isNegative ? '-' : ''}₹${formatted}.${decimalPart}`;
};

/**
 * Format numbers in Indian style (lakhs, crores)
 * Example: 123456 -> 1,23,456
 */
export const formatIndianNumber = (number) => {
    if (number === null || number === undefined) return '0';

    const isNegative = number < 0;
    const absNumber = Math.abs(number);
    const numberStr = Math.floor(absNumber).toString();

    if (numberStr.length <= 3) {
        return `${isNegative ? '-' : ''}${numberStr}`;
    }

    const lastThree = numberStr.slice(-3);
    const remaining = numberStr.slice(0, -3);

    const formatted = remaining.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + lastThree;

    return `${isNegative ? '-' : ''}${formatted}`;
};

/**
 * Format date for display
 */
export const formatDate = (date) => {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
};

/**
 * Format date for input fields (YYYY-MM-DD)
 */
export const formatDateForInput = (date) => {
    if (!date) return '';
    const d = new Date(date);
    return d.toISOString().split('T')[0];
};

/**
 * Get month name
 */
export const getMonthName = (month) => {
    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months[month - 1] || '';
};
