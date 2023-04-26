import React, { useState, useEffect, Component } from "react";
import ReactDOM from "react-dom/client";
import "../index.css";
import "../css/notifications.css";
import jwt_decode from "jwt-decode";
import axios from 'axios';


function NotificationList() {
    const [notifications, setNotifications] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [hasNextPage, setHasNextPage] = useState(false);
    const [hasPreviousPage, setHasPreviousPage] = useState(false);
    const [stateType, setStateType] = useState("");

    const handleNextPage = () => {
        if (hasNextPage) {
          setCurrentPage(currentPage + 1);
        }
      };
      const handlePreviousPage = () => {
        if (hasPreviousPage) {
          setCurrentPage(currentPage - 1);
        }
      };

    useEffect(() => {
    let url = "http://localhost:8000/notifications/all/";
    url += "?page=" + parseInt(currentPage);

    if (stateType === "U") {
        url += "&state=U";
    } else if (stateType === "R") {
        url += "&state=R";
    }

    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "http://localhost:3000/login/";
        return;
    }
    var decoded = jwt_decode(token);
    const user_id = decoded.user_id;

    fetch(url, {
        headers: { Authorization: "Bearer " + token },
    })
        .then((response) => response.json())
        .then((data) => {
        setNotifications(data.data);
        // setCurrentPage(data.page.current);
        setHasNextPage(data.page.has_next);
        setHasPreviousPage(data.page.has_previous);
        });
    }, [currentPage, stateType]);

    return (
<div>
      <br></br>
      <h1>Notifications</h1>

      <br></br>
      
      <h5 style={{ textAlign: "center" }}>Filter by State:</h5>
      <div className="filter-bar">
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("U");setCurrentPage(1);}}
          className={stateType === "U" ? "clicked" : ""}
        >
          Unread
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("R");setCurrentPage(1);}}
          className={stateType === "R" ? "clicked" : ""}
        >
          Read
        </button>
        <button
          className="clear-all"
          style={{ width: "8rem", color: "#373A36" }}
          onClick={() => {
            setStateType("");
            setCurrentPage(1);
          }}
        >
          Clear Filter
        </button>
      </div>
      <div style={{ padding: "0.5rem" }}></div>
      <h5 style={{ textAlign: "center" }}>Clear Notifications:</h5>
      <div className="filter-bar">
        <button onClick={clearNotifications}
          style={{ width: "auto", color: "#373A36" }}
          className="clear-notif"
        >
          Clear All Read Notifications
        </button>
      </div>

      <div style={{ padding: "0.5rem" }}></div>
      <h4 style={{ textAlign: 'center', marginBottom: '5rem'  }} className={notifications.length === 0 ? "" : "removed"}>No notifications found</h4>

      {notifications.map((notification) => (
        <div key={notification.id} className={`col-md-7 mb-4 mx-auto`}>
            <div className="card">
          <div className="card-body">
            <button 
            onClick={() => {markNotificationAsRead(notification.id)}}
            className={`${getStateClass(notification.state)}`}>
                {getStateClass(notification.state)}
              </button>
              <h5 className="card-title">{convertDateTime(notification.created_at)}</h5>
            <p className="card-text">{notification.content}</p>
            <p className="card-text">Reservation ID: {notification.reservation}</p>
            <sub className="card-text">Notification ID: {notification.id}</sub>
            </div>
            </div>
            
            </div>

      ))}

      <div className="filter-bar">
        <button
          onClick={handlePreviousPage}
          className={hasPreviousPage ? "" : "hidden"}
          disabled={!hasPreviousPage}
        >
          Previous
        </button>
        <b>&nbsp;Page {currentPage}&nbsp; </b>
        <button
          onClick={handleNextPage}
          className={hasNextPage ? "" : "hidden"}
          disabled={!hasNextPage}
        >
          Next
        </button>
      </div>
      <div style={{ padding: "0.5rem" }}></div>
    </div>
    )
}

function convertDateTime(timestamp) {
    const date = new Date(timestamp);
    const formattedDate = date.toISOString().replace('T', ' ').replace(/\.\d{3}Z/, ' UTC');
    return(formattedDate);
  }

function getStateClass(state) {
    if (state === 'R') {
        return 'Read';
    } else if (state === 'U') {
        return 'Unread';
    }
}

const markNotificationAsRead = (notificationId) => {

    const token = localStorage.getItem("token");
    const url = "http://localhost:8000/notifications/" + parseInt(notificationId) + '/';
  
    axios
      .patch(
        url,
        {},
        {
          headers: {
            Authorization: "Bearer " + token
          },
        }
      )
      .then((response) => {
        // Handle successful response here, e.g. show a success message to the user
        window.location.href = "http://localhost:3000/notifications/all/";

      })
      .catch((error) => {
        console.error(error);
        // Handle error
      });
  }
const clearNotifications = () => {
  const token = localStorage.getItem("token");
    fetch('http://localhost:8000/notifications/clear/', {
      method: 'DELETE',
      headers: {
        Authorization: "Bearer " + token
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to clear notifications');
      }
      window.location.href = "http://localhost:3000/notifications/all/";
    })
    .catch(error => {
      console.error(error);
      // handle error
    });
  };
export default NotificationList;