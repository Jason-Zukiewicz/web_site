const Tweets = ({ tweets, getTweets }) => {
    return (
        <div>
            <p> This will be a tweet</p>
            <tbody>
                {Object.entries(tweets).map(([k, v]) => <Tweet key={k} tweetId={k} {...v} getTweets={getTweets} />)}
            </tbody>
        </div>
    );
};

const Tweet = ({ tweetId, authorId, msg }) => {
    return (
        <tr>
            <td>{authorId}</td>
            <td>{msg}</td>
        </tr>
    );
};

export default Tweets;