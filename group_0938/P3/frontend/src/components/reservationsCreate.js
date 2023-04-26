import "../index.css";
import "../css/reservations.css";
import ReactDOM from "react-dom";
import React, { useState } from "react";

function CreateReservation() {
    const [propertyId, setPropertyId] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);
  
    const handleSubmit = (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        if (!token) {
            window.location.href = "http://localhost:3000/login/";
            return;
          }
        fetch('http://localhost:8000/reservations/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: "Bearer " + token,
          },
          body: JSON.stringify({
            property: propertyId,
            start_date: startDate,
            end_date: endDate
          })
        })
        .then(response => {
            if (!response.ok) {
                console.log(response.error);
                setErrorMessage('Reservation creation failed. Please ensure the property ID points to an existing property, and the start and end date equate to one or more (consecutive) availability time ranges of that property.');
              throw new Error(response.status);
              
            }
            return response.json();
          })
        .then(data => {
          console.log('Success:', data);
          // do something with the response data
            window.location.href = "http://localhost:3000/reservations/all/";
        })
        .catch((error) => {
            // if (error.response && error.response.data && error.response.data.error) {
            //   setErrorMessage(error.response.data.error);
            // } else {
            //   setErrorMessage('An error occurred while creating the reservation.');
            // }
            
          });
      };
  
    return (
        <div>
            <h1>Create a Reservation:</h1>
      <form onSubmit={handleSubmit} className={`col-md-7 mb-4 mx-auto`} style={{ padding: "0.5rem" }}>
        <div ></div>
        <label htmlFor="property-id">Property ID:</label>
        <input 
          type="number" 
          id="property-id" 
          name="propertyId" 
          value={propertyId} 
          onChange={(e) => setPropertyId(e.target.value)} 
          required 
        />
        <div style={{ padding: "0.5rem" }}></div>
        <label htmlFor="start-date">Start Date:</label>
        <input 
          type="date" 
          id="start-date" 
          name="startDate" 
          value={startDate} 
          onChange={(e) => setStartDate(e.target.value)} 
          required 
        />
        <div style={{ padding: "0.5rem" }}></div>
        <label htmlFor="end-date">End Date:</label>
        <input 
          type="date" 
          id="end-date" 
          name="endDate" 
          value={endDate} 
          onChange={(e) => setEndDate(e.target.value)} 
          required 
        />
        <div style={{ padding: "0.5rem" }}></div>
        <button type="submit">Submit</button>
        <div style={{ padding: "0.5rem" }}></div>
        {errorMessage && <h5>{errorMessage}</h5>}
      </form>
      </div>
    );
  }
  
  export default CreateReservation;