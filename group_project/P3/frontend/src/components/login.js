import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../css/login.css';
import '../index.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const navigate = useNavigate()
    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/user/login/', {
                username: username,
                password: password,
            });

            if (response.data) {
                localStorage.setItem('token', response.data.access);
                setIsLoggedIn(true);
            } else {
                setError('Invalid username or password');
            }
        } catch (error) {
            setError('Invalid username or password');
        }
    };

    if (isLoggedIn) {
        navigate("/reservations/all/");
        return null;
    }

    return (
        <div className='root'>

            <div className="container d-flex flex-col justify-content-center mt-5">

                <form className="w-50" onSubmit={handleSubmit}>
                    <h1> Log In</h1>
                    <div className="form-group">
                        <label htmlFor="exampleInputEmail1">Username</label>
                        <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" value={username} onChange={(e) => setUsername(e.target.value)} required />
                        <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                    </div>
                    <div className="form-group mb-4">
                        <label htmlFor="exampleInputPassword1">Password</label>
                        <input type="password" className="form-control" id="exampleInputPassword1" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    {error && <p className="error-message">{error}</p>}
                    <label htmlFor="save" className="button1">Log in</label>
                    <input type="submit" id="save" hidden />

                    <h6 className="mt-4"> Don't have an account? <a href="/signup"> Sign Up Here</a></h6>
                </form>
            </div>
        </div>
    );
};

export default Login;