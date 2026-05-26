function OrderItem({ item }) {
    return (
        <div style={{
            border: "1px solid #ddd",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "8px"
        }}
        >

            <p>
                <b>Product: {item.product_name}</b>
            </p>

            <p>
                <b>Quantity: {item.quantity}</b>
            </p>


            <p>
                <b>Price: ${item.price}</b>
            </p>

            <p>
                <b>Subtotal: ${item.subtotal}</b>
            </p>
        </div>
    )
}

export default OrderItem