import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../index.css';
import '../css/signup.css';


const isUsernameValid = (username) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(username);
};

const isPhoneValid = (phone) => {
    const phoneRegex = /^\+\d{11}$/;
    return phoneRegex.test(phone);
};

const isNonEmpty = (value) => {
    return value && value.trim().length > 0;
};

const Signup = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        username: '',
        password: '',
        phone: '',
    });

    const [error, setError] = useState(null);
    const [successfulSignup, setSuccessfulSignup] = useState(false);

    const handleChange = (e) => {
        const value = e.target.type === 'file' ? e.target.files[0] : e.target.value;
        setFormData({ ...formData, [e.target.name]: value });
    };

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!isUsernameValid(formData.username)) {
            setError({ field: 'username', message: 'Username is not valid' });
            return;
        }

        if (!isPhoneValid(formData.phone)) {
            setError({ field: 'phone', message: 'Phone number is not valid.' });
            return;
        }

        const nonEmptyFields = ['first_name', 'last_name', 'password', 'phone', 'username'];
        for (const field of nonEmptyFields) {
            if (!isNonEmpty(formData[field])) {
                setError({ field, message: `${field} must not be empty.` });
                return;
            }
        }

        const data = new FormData();
        Object.entries(formData).forEach(([key, value]) => {
            // Check if the key is not profile_pic or if there is a file in profile_pic field
            if (key !== "profile_pic" || (key === "profile_pic" && value)) {
                data.append(key, value);
            }
        });

        try {
            const response = await axios.post('http://localhost:8000/user/signup/', data);
            console.log(response.data);
            setSuccessfulSignup(true);
        } catch (error) {
            console.error('Error during signup:', error.response.data);
            setError({ field: 'server', message: 'Error during signup. Please try again later.' });
        }
    };

    if (successfulSignup) {
        navigate('/login/');
        return null;
    }

    return (
        <>
            <div class="root">
                <div className="vertical_space"></div>

                <div className="grid-container">
                    <h1>Sign Up</h1>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="grid-container">
                        <div className="grid-item1">
                            <label htmlFor='first_name' className='form-label'>First Name:</label>
                            <input
                                type="text"
                                name="first_name"
                                placeholder="John"
                                onChange={handleChange}
                            />
                            {error && error.field === 'first_name' && (
                                <p className="error-message">{error.message}</p>
                            )}

                            <label htmlFor='last_name' className='form-label'>Last Name:</label>
                            <input
                                type="text"
                                name="last_name"
                                placeholder="Doe"
                                onChange={handleChange}
                            />
                            {error && error.field === 'last_name' && (
                                <p className="error-message">{error.message}</p>
                            )}

                            <label htmlFor='username' className='form-label'>Email Address:</label>
                            <small id="emailHelp" className="form-text text-muted">
                                This will also be your username for future log-ins.
                            </small>
                            <input
                                type="email"
                                name="username"
                                placeholder="john.doe@gmail.com"
                                onChange={handleChange}
                            />
                            {error && error.field === 'username' && (
                                <p className="error-message">{error.message}</p>
                            )}

                            <label htmlFor='password' className='form-label'>Password:</label>
                            <input
                                type="password"
                                name="password"
                                onChange={handleChange}
                            />
                            {error && error.field === 'password' && (
                                <p className="error-message">{error.message}</p>
                            )}

                            <label htmlFor='phone' className='form-label'>Phone Number:</label>
                            <input
                                type="text"
                                name="phone"
                                placeholder="+16478887777"
                                onChange={handleChange}
                            />
                            {error && error.field === 'phone' && (
                                <p className="error-message">{error.message}</p>
                            )}

                            <label htmlFor="img" className=" form-label mb-4">
                                Upload Profile Picture
                            </label>
                            <input
                                type="file"
                                id="img"
                                name="profile_pic"
                                accept="image/*"
                                onChange={handleChange}
                            />

                            <button type="submit" className="form-label button1">
                                Sign Up
                            </button>
                            {error && error.field === 'server' && (
                                <p className="error-message">{error.message}</p>
                            )}

                        </div>
                    </div>
                </form>
            </div>
        </>
    );
};

export default Signup;
