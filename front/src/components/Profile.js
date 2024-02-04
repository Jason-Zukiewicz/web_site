import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { getter } from '../Utils';
import { useParams } from 'react-router-dom';

import Tweets from './Tweet';

const Profile = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { userId } = useParams(); // From Route

    const [tweets, setTweets] = useState(null);
    useEffect(() => { getTweets(); }, []);
    const getTweets = () => {
        getter(`tweets/${userId}`, setTweets, setLoading, setError);
    };

    return (
        <div>
            {loading && <p>Loading..tweets</p>}
            {error && <p>Failed to load!</p>}
            <h2>User Profile: {userId}</h2>
            <div>
                <div className="content">
                    {!loading && tweets && <Tweets tweets={tweets} getTweets={getTweets} />}

                </div>
            </div>
        </div>
    );
};


export default Profile;