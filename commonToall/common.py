RETAILER_STATUS = (
    ("CREATED", "Created"),
    ("PENDING", "Pending Approval"),
    ("KYCAPPROVED", "KYC Approved"),
    ("KYCREJECTED", "KYC Rejected"),
    ("APPROVED", "Approved"),
)

BUSINESS_STATUS = (
    ("NOTREGISTERED", "Not Registered"),
    ("REGISTERED", "Registered")
)

RETAILER_NOTIFICATION_STATUS = (
    ("NEW", "New Request"),
    ("OLD", "Old Request"),
    ("ACCEPT", "Accepted Request"),
    ("REJECT", "Rejected Request"),
    ("SAVE", "Save For Later")
)

RETAILER_PLAN= (
    ('CASH', 'Cash'),
    ('PLATINUM', 'Platinum'),
    ('DIAMOND', 'Diamond'),
    ('GOLD', 'Gold'),
    ('BRONZE', 'Bronze')
)

PAYMENT_TYPE = (
    ("CASH", "Cash"),
    ("CREDIT", "Credit"),
    ('UPI', 'UPI'),
    ('CHEQUE', 'Cheque'),
    ('NEFT/RTGS', 'NEFT/RTGS')
)
PAYMENT_STATUS = (
    ("PENDING", "Pending"),
    ("COMPLETED", "Completed")
)

ORDER_STATUS = (
    ("PENDING", 'Pending'),
    ("APPROVED", 'Approved'),
    ('REJECTED', 'Rejected'),
    ('INPROGRESS', 'InProgress'),
    ('SUCCESS', 'Success'),
    ('OUTFORDELIVERY', 'Out for Delivery')
)