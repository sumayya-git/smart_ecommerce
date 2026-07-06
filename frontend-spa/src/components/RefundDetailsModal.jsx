function RefundDetailsModal() {
    return (
        <div
            style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                background: "rgba(0,0,0,0.5)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 1000,
            }}
        >
            <div
                style={{
                    background: "white",
                    padding: "25px",
                    borderRadius: "10px",
                    width: "400px",
                }}
            >
                <h2>Refund Details</h2>

                <p>Form will be added in next step...</p>

                <button>
                    Close
                </button>
            </div>
        </div>
    );
}

export default RefundDetailsModal;