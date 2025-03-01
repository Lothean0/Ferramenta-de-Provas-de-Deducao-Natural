import { useEffect, useState } from 'react';
import '../styles/PropositionLogicBody.css';
import axios from 'axios';

function PropositionalLogicBody() {
    const [array, setArray] = useState([]);
    const [expression, setExpression] = useState("");
    const [rule, setRule] = useState("");

    async function getUser() {
        try {
            const response = await axios.get("http://127.0.0.1:3000/api/users");
            setArray(response.data.users);
        } catch (error) {
            console.error("Error fetching users:", error);
            setArray([]);
        }
    }

    useEffect(() => {
        getUser();
    }, []);

    async function sendExpressionAndRule() {
        if (!expression || !rule) {
            alert("Both expression and rule are required!");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:3000/api/checkExpression", {
                expression,
                rule
            });
            console.log("Server response:", response.data);
            window.confirm("Message sent successfully!");
            setExpression("");
            setRule("");
        } catch (error) {
            console.error("Error sending data:", error);
            alert("Failed to send data");
        }
    }

    return (
        <>
            <input
                className='input-container'
                placeholder="Enter expression..."
                value={expression}
                onChange={(e) => setExpression(e.target.value)}
            />

            <input
                className='input-container'
                placeholder="Enter rule..."
                value={rule}
                onChange={(e) => setRule(e.target.value)}
            />

            <button onClick={sendExpressionAndRule}>Send</button>

            <ul>
                {array.map((user, index) => (
                    <li key={index}>{user}</li>
                ))}
            </ul>
        </>
    );
}

export default PropositionalLogicBody;
