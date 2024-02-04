import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Home from './components/Home'; // Import your Home component
import About from './components/About'; // Import your About component
import Login from './components/Login'; // Import your About component
import Signup from './components/Signup'; // Import your About component

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/about" component={About} />
                <Route path="/Login" component={Login} />
                <Route path="/Signup" component={Signup} />
            </Switch>
        </Router>
    );
}

export default App;