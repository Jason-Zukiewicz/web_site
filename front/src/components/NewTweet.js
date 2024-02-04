import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Assuming you are using React Router
import { poster, getCookie, setCookie } from '../Utils';

const NewTweet = () => {
    const [authorID, setAuthorID] = useState('');
    const [msg, setMsg] = useState('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const history = useHistory();

    // Check Cookies to make sure logged in
    useEffect(() => {
        const authorIDCookie = getCookie('userId'); // Assuming your user ID cookie is named 'userId'
        if (!authorIDCookie) {
            history.push('/login');
        } else {
            setAuthorID(authorIDCookie);
        }
    }, [history]);

    // Post To Back
    const handleTweet = async (e) => {
        e.preventDefault();

        if (!authorID || !msg) {
            setError('Author ID and Message are required');
            return;
        }

        setError(null);

        const data = { authorID, msg }; // Change userId to authorID

        setLoading(true);

        try {
            await poster('tweet/', data, () => {
                console.log('Tweet successful!');
                setLoading(false);
                history.push('/');
            });
        } catch (error) {
            setLoading(false);
            setError('Tweet failed. Please try again.');
        }
    };

    // Loading
    useEffect(() => {
        // Set a timeout to handle cases where there's no response in 5 seconds
        const timeoutId = setTimeout(() => {
            if (loading) {
                setLoading(false);
                setError('Tweet timed out. Please try again.');
            }
        }, 5000);

        return () => clearTimeout(timeoutId);
    }, [loading]);

    // HTML
    return (
        <div>
            <h1>This is the Tweet Creation Page</h1>
            <form onSubmit={handleTweet}>
                <ul>
                    <li>
                        <label htmlFor="Message">Message:</label>
                    </li>
                    <li>
                        <input
                            type="text"
                            id="message"
                            name="message"
                            value={msg}
                            onChange={(e) => setMsg(e.target.value)}
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

export default NewTweet;