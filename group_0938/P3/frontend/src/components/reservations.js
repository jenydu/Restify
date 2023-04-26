import React, { useState, useEffect, Component } from "react";
import ReactDOM from "react-dom/client";
import "../index.css";
import "../css/reservations.css";
import jwt_decode from "jwt-decode";
import axios from 'axios';

function ReservationList() {
  const [reservations, setReservations] = useState([]);
  const [userType, setUserType] = useState("");
  const [stateType, setStateType] = useState("");

  const [currentPage, setCurrentPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [hasPreviousPage, setHasPreviousPage] = useState(false);

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
  function Reservation({ reservation }) {
    const [properties, setProperties] = useState(null);
    const [host, setHost] = useState(null);
    const [guest, setGuest] = useState(null);
    const [user_id, setUser] = useState(0);
  
    const [requestCancel, setRequestCancel] = useState(false);
    const [approvePending, setApprovePending] = useState(false);
    const [denyPending, setDenyPending] = useState(false);
    const [terminate, setTerminate] = useState(false);
    const [approveCancel, setApproveCancel] = useState(false);
    const [denyCancel, setDenyCancel] = useState(false);
  
    useEffect(() => {
      const token = localStorage.getItem("token");
      var decoded = jwt_decode(token);
      setUser(decoded.user_id);
  
      fetch(`http://localhost:8000/properties/${reservation.property}/`, {
        headers: { Authorization: "Bearer " + token },
      })
        .then((response) => response.json())
        .then((data) => setProperties(data));
  
      fetch(`http://localhost:8000/user/${reservation.host}/`, {
        headers: { Authorization: "Bearer " + token },
      })
        .then((response) => response.json())
        .then((data) => setHost(data));
  
      fetch(`http://localhost:8000/user/${reservation.user}/`, {
        headers: { Authorization: "Bearer " + token },
      })
        .then((response) => response.json())
        .then((data) => setGuest(data));
    }, [reservation]);
  
    if (!properties || !host || !guest) {
      return <div> </div>;
    }
    return (
      <div key={reservation.id} className={`col-md-7 mb-4 mx-auto`}>
        <div className="card">
          <div className="card-body">
          <sub className="card-title">Reservation ID: {reservation.id}</sub>
            <h5 className="card-text">
              {properties.unit_num} {properties.street}, {properties.city},{" "}
              {properties.province}, {properties.country}
            </h5>
            <h5 className="card-text">
              {reservation.start_date} — {reservation.end_date}
            </h5>
            
            <div style={{ padding: "0.5rem" }}></div>
            <p className="card-text">
              <b>Host: </b>
              {host.first_name} {host.last_name}
            </p>
            <p className="card-text">
              <b>Guest: </b>
              {guest.first_name} {guest.last_name}
            </p>
            <p className="card-text">
              <b>Total Price: </b> $ {reservation.price}
            </p>
            <div style={{ padding: "0.5rem" }}></div>
            <div className="filter-bar">
              <div className={`${getStateClass(reservation.state)}`}>
                {getStateClass(reservation.state)}
              </div>
              <div style={{ padding: "0.5rem" }}></div>
              {/* action buttons */}
              <button
                onClick={() => setRequestCancel(true)}
                className={
                  parseInt(user_id) == parseInt(reservation.user) &&
                  reservation.state == "Ap"
                    ? "action-button"
                    : "removed"
                }
              >
                Request Cancellation
              </button>
              <div className={requestCancel ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b>
                  Are you sure you want to request a cancellation? Note that the
                  host will need to approve your request for this reservation to
                  be cancelled.
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handleCancelReservation(reservation.id)} 
                className="cancel-btn">Confirm</button>
              </div>

              <button
              onClick={() => setTerminate(true)}
                className={
                  parseInt(user_id) == parseInt(reservation.host) &&
                  reservation.state == "Ap"
                    ? "action-button"
                    : "removed"
                }
              >
                Terminate
              </button>
              <div className={terminate ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b className="card-text">
                  Are you sure you want to terminate this reservation? This action cannot be undone.
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handleTerminate(reservation.id)} 
                className="cancel-btn">Confirm</button>
              </div>

              <button onClick={() => {setApprovePending(true);setDenyPending(false);}}
                className={
                  parseInt(user_id) == parseInt(reservation.host) &&
                  reservation.state == "Pd"
                    ? "action-button"
                    : "removed"
                }
              >
                Approve
              </button>
              <button onClick={() => {setDenyPending(true);setApprovePending(false);}}
                className={
                  parseInt(user_id) == parseInt(reservation.host) &&
                  reservation.state == "Pd"
                    ? "action-button"
                    : "removed"
                }
              >
                Deny
              </button>
              <div className={approvePending ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b className="card-text">
                  Approve this reservation? 
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handlePendingAction(reservation.id, 'approve')} 
                className="cancel-btn">Confirm</button>
              </div>
              <div className={denyPending ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b className="card-text">
                  Deny this reservation? This action cannot be undone.
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handlePendingAction(reservation.id, 'deny')} 
                className="cancel-btn">Confirm</button>
              </div>

              <button onClick={() => {setDenyCancel(false); setApproveCancel(true);}}
                className={
                  parseInt(user_id) == parseInt(reservation.host) &&
                  reservation.state == "Pc"
                    ? "action-button"
                    : "removed"
                }
              >
                Approve
              </button>
              <button onClick={() => {setDenyCancel(true); setApproveCancel(false);}}
                className={
                  parseInt(user_id) == parseInt(reservation.host) &&
                  reservation.state == "Pc"
                    ? "action-button"
                    : "removed"
                }
              >
                Deny
              </button>
              <div className={approveCancel ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b className="card-text">
                  Approve the guest's cancellation request? the reservation will be canceled.
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handleCancelAction(reservation.id, 'approve')} 
                className="cancel-btn">Confirm</button>
              </div>
              <div className={denyCancel ? "warning-msg" : "removed"}>
                <div style={{ padding: "0.25rem" }}></div>
                <b className="card-text">
                  Deny the guest's cancellation request? the reservation will return to the 'Approved' state.
                </b>
                <div style={{ padding: "0.25rem" }}></div>
                <button onClick={()=> handleCancelAction(reservation.id, 'deny')} 
                className="cancel-btn">Confirm</button>
              </div>
              
            </div>
          </div>
        </div>
      </div>
    );
  }

  ///////////////////////////////////////////////
  const handleCancelReservation = (rid) => { 
    const token = localStorage.getItem("token");
    axios.put(`http://localhost:8000/reservations/cancel/`, { id: rid.toString() }, {
        headers: { Authorization: "Bearer " + token }
    })
      .then(response => {
        // Handle successful response here, e.g. show a success message to the user
        window.location.href = "http://localhost:3000/reservations/all/";
      })
      .catch(error => {
        console.error(error);
        // Handle error here, e.g. show an error message to the user
      });
  }

  const handleTerminate = (rid) => { 
    const token = localStorage.getItem("token");
    axios.put(`http://localhost:8000/reservations/terminate/`, { id: rid.toString() }, {
        headers: { Authorization: "Bearer " + token }
    })
      .then(response => {
        // Handle successful response here, e.g. show a success message to the user
        window.location.href = "http://localhost:3000/reservations/all/";
      })
      .catch(error => {
        console.error(error);
        // Handle error here, e.g. show an error message to the user
      });
  }

  const handlePendingAction = (rid, apprdeny) => { 
    // console.log(apprdeny);

    const token = localStorage.getItem("token");
    axios.put(`http://localhost:8000/reservations/approve/pending/`, { id: rid.toString(), action: apprdeny }, {
        headers: { Authorization: "Bearer " + token }
    })
      .then(response => {
        // Handle successful response here, e.g. show a success message to the user
        window.location.href = "http://localhost:3000/reservations/all/";
      })
      .catch(error => {
        console.error(error);
        // Handle error here, e.g. show an error message to the user
      });
  }

  const handleCancelAction = (rid, apprdeny) => { 
    console.log(apprdeny);
    const token = localStorage.getItem("token");
    axios.put(`http://localhost:8000/reservations/approve/cancel/`, { id: rid.toString(), action: apprdeny.toString() }, {
        headers: { Authorization: "Bearer " + token }
    })
      .then(response => {
        // Handle successful response here, e.g. show a success message to the user
        window.location.href = "http://localhost:3000/reservations/all/";
      })
      .catch(error => {
        console.error(error);
        // Handle error here, e.g. show an error message to the user
      });
  }
  /////////////////////////////////////////////////
  
  useEffect(() => {
    let url = "http://localhost:8000/reservations/all/`";
    url += "?page=" + parseInt(currentPage);
    if (userType === "guest") {
      url =
        "http://localhost:8000/reservations/all/" +
        "?page=" +
        parseInt(currentPage) +
        "&user_type=guest";
    } else if (userType === "host") {
      url =
        "http://localhost:8000/reservations/all/" +
        "?page=" +
        parseInt(currentPage) +
        "&user_type=host";
    } else {
      url =
        "http://localhost:8000/reservations/all/" +
        "?page=" +
        parseInt(currentPage);
    }

    if (stateType === "Pd") {
      url += "&state=Pd";
    } else if (stateType === "Dn") {
      url += "&state=Dn";
    } else if (stateType === "Ex") {
      url += "&state=Ex";
    } else if (stateType === "Ap") {
      url += "&state=Ap";
    } else if (stateType === "Pc") {
      url += "&state=Pc";
    } else if (stateType === "Cc") {
      url += "&state=Cc";
    } else if (stateType === "Tm") {
      url += "&state=Tm";
    } else if (stateType === "Cm") {
      url += "&state=Cm";
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
        setReservations(data.data);
        // setCurrentPage(data.page.current);
        setHasNextPage(data.page.has_next);
        setHasPreviousPage(data.page.has_previous);
      });
  }, [userType, currentPage, stateType]);

  return (
    <div>
      <br></br>
      <h1>My Reservations</h1>

      <br></br>
      <h5 style={{ textAlign: "center" }}>Filter by User Type:</h5>
      <div className="filter-bar">
        <button
          onClick={() => {setUserType("guest");setCurrentPage(1);}}
          className={userType === "guest" ? "clicked" : ""}
        >
          Guest
        </button>
        <button
          onClick={() => {setUserType("host");setCurrentPage(1);}}
          className={userType === "host" ? "clicked" : ""}
        >
          Host
        </button>
      </div>
      <div style={{ padding: "0.5rem" }}></div>
      <h5 style={{ textAlign: "center" }}>Filter by Reservation State:</h5>
      <div className="filter-bar">
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Pd");setCurrentPage(1);}}
          className={stateType === "Pd" ? "clicked" : ""}
        >
          Pending
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Dn");setCurrentPage(1);}}
          className={stateType === "Dn" ? "clicked" : ""}
        >
          Denied
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Ex");setCurrentPage(1);}}
          className={stateType === "Ex" ? "clicked" : ""}
        >
          Expired
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Ap");setCurrentPage(1);}}
          className={stateType === "Ap" ? "clicked" : ""}
        >
          Approved
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Pc");setCurrentPage(1);}}
          className={stateType === "Pc" ? "clicked" : ""}
        >
          Pending Cancellation
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Cc");setCurrentPage(1);}}
          className={stateType === "Cc" ? "clicked" : ""}
        >
          Cancelled
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Tm");setCurrentPage(1);}}
          className={stateType === "Tm" ? "clicked" : ""}
        >
          Terminated
        </button>
        <button
          style={{ width: "auto" }}
          onClick={() => {setStateType("Cm");setCurrentPage(1);}}
          className={stateType === "Cm" ? "clicked" : ""}
        >
          Completed
        </button>
      </div>
      <div style={{ padding: "0.5rem" }}></div>
      <div className="filter-bar">
        <button
          className="clear-all"
          style={{ width: "10rem", color: "#373A36" }}
          onClick={() => {
            setUserType("");
            setStateType("");
            setCurrentPage(1);
          }}
        >
          CLEAR ALL
        </button>
      </div>

      <div style={{ padding: "0.5rem" }}></div>
      <h4 style={{ textAlign: 'center', marginBottom: '5rem'  }} className={reservations.length === 0 ? "" : "removed"}>No reservations found</h4>

      {reservations.map((reservation) => (
        <Reservation key={reservation.id} reservation={reservation} />
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
  );
}



function getStateClass(state) {
  switch (state) {
    case "Pd":
      return "PENDING";
    case "Dn":
      return "DENIED";
    case "Ex":
      return "EXPIRED";
    case "Ap":
      return "APPROVED";
    case "Cc":
      return "CANCELED";
    case "Tm":
      return "TERMINATED";
    case "Cm":
      return "COMPLETED";
    case "Pc":
      return "PENDING-CANCELLATION";
    default:
      return "";
  }
}

export default ReservationList;
