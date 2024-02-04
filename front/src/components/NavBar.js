import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';
import { getCookie, deleteCookie } from '../Utils';

const NavBar = () => {
    const username = getCookie('userName');
    const userId = getCookie('userId');

    const handleLogout = () => {
        deleteCookie('userName');
        deleteCookie('userId');
        window.location.reload()
    };


    return (
        <nav>
            <ul className="nav-list">
                <li className="nav-item"><Link to="/" className="nav-link">Home</Link></li>
                <li className="nav-item"><Link to={`/profile/${userId}`} className="nav-link">Profile</Link></li>
                <li className="nav-item"><Link to="/tweet" className="nav-link">Tweet</Link></li>

                {!username && (
                    <>
                        <li className="nav-item"><Link to="/login" className="nav-link">Login</Link></li>
                        <li className="nav-item"><Link to="/signup" className="nav-link">Signup</Link></li>
                    </>
                )}
                {username && (
                    <>
                        <li className="nav-item"><span className="nav-link">{username}</span></li>
                        <li className="nav-item">
                            <Link to="/login" className="nav-link" onClick={handleLogout}>
                                Logout
                            </Link>
                        </li>

                    </>
                )}

            </ul>
        </nav>
    );
};

export default NavBar;