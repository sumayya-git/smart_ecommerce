function PaymentBadge({ order }) {
    const paymentStatus = order?.payment_status?.toUpperCase()
    const paymentMethod = order?.payment_method?.toUpperCase()

    const backgroundColor = paymentStatus === "PAID" ? "green" : paymentStatus === "PENDING" ? "orange" : "blue"


    const text = paymentStatus === "PAID" ? "PAID" : paymentMethod === "COD" ? "COD" : "PENDING"


    return(
        <span style={{
            padding: "4px 10px",
            borderRadius: "12px",
            fontSize: "12px",
            fontWeight: "bold",
            color: "white",
            backgroundColor
        }}
        >
            {text}

        </span>
    )

}

export default PaymentBadge