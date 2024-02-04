import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Assuming you are using React Router
import { poster } from '../Utils';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const history = useHistory();

    const handleSignup = async (e) => {
        e.preventDefault();

        // Check if username and password are provided
        if (!username || !password1 || !password2) {
            setError('Username and password are required');
            return;
        }

        // Clear previous error
        setError(null);

        // Prepare data for the POST request
        const data = { username, password1, password2 };

        // Set loading to true while the request is in progress
        setLoading(true);

        try {
            // Make the POST request using the poster utility function
            await poster('signup/', data, () => {
                // Callback function to handle the response
                console.log('Signup successful!');
                setLoading(false);

                // Redirect to the home page upon successful login
                history.push('/');
            });
        } catch (error) {
            // Handle errors or timeout here
            setLoading(false);
            setError('Login failed. Please try again.');
        }
    };

    useEffect(() => {
        // Set a timeout to handle cases where there's no response in 5 seconds
        const timeoutId = setTimeout(() => {
            if (loading) {
                setLoading(false);
                setError('Signup timed out. Please try again.');
            }
        }, 5000);

        return () => clearTimeout(timeoutId);
    }, [loading]);
    return (
        <div>
            <h1>This is the Login page</h1>
            <form onSubmit={handleSignup}>
                <ul>
                    <li>
                        <label htmlFor="username">Username:</label>
                    </li>
                    <li>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </li>

                    <li>
                        <label htmlFor="password1">Password1:</label>
                    </li>
                    <li>
                        <input
                            type="password1"
                            id="password1"
                            name="password1"
                            value={password1}
                            onChange={(e) => setPassword1(e.target.value)}
                            required
                        />
                    </li>

                    <li>
                        <label htmlFor="password2">Password2:</label>
                    </li>
                    <li>
                        <input
                            type="password2"
                            id="password2"
                            name="password2"
                            value={password2}
                            onChange={(e) => setPassword2(e.target.value)}
                            required
                        />
                    </li>

                    <li>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </li>
                </ul>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
};

export default Signup;