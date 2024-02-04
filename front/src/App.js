import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Home from './components/Home';
import Login from './components/Login';
import Signup from './components/Signup';
import NavBar from './components/NavBar';
import Profile from './components/Profile';
import NewTweet from './components/NewTweet';

const App = () => {
    return (
        <Router>
            <div>
                <NavBar />
                <Switch>
                    <Route path="/login" component={Login} />
                    <Route path="/signup" component={Signup} />
                    <Route path="/Tweet" component={NewTweet} />
                    <Route path="/profile/:userId" component={Profile} />
                    <Route path="/" component={Home} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;