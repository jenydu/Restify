import logo from './logo.svg';
import './index.css';
import './App.css';

// routing
import { Routes, Route } from 'react-router-dom';
import ReservationList from './components/reservations';
import CreateReservation from './components/reservationsCreate';
import NotificationList from './components/notifications';
import Login from './components/login';
import Signup from './components/signup';


// any elements added here will appear on all pages
const App = () => {
   return (
      <>
         <nav className="navbar bg-primary navbar-expand-lg bg-body-tertiary fixed-top" data-bs-theme="dark">
            <div className="container-fluid">
               <a className="navbar-brand button_top" href="#"><i className="fa fa-plane" aria-hidden="true"></i>Restify</a>
               {/* <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                  <span className="navbar-toggler-icon"></span>
               </button> */}
               {/* <a className="" href="http://localhost:3000/reservations/all/">Create a Reservation</a>
               <a className="" href="http://localhost:3000/reservations/all/">My Reservations</a>
               <a className="" href="http://localhost:3000/notifications/all/">Notifications</a> */}
              <div class="dropdown">
                  <input type="checkbox" id="dropdown-checkbox" class="dropdown-checkbox" />
                  <label for="dropdown-checkbox" class="dropdown-label">Menu</label>
                  <div class="dropdown-content">
                     <a href="http://localhost:3000/login/">Log In/Sign Up</a>
                     <a href="http://localhost:3000/notifications/all/">Notifications</a>
                     <a href="http://localhost:3000/reservations/create/">Create a Reservation</a>
                     <a href="http://localhost:3000/reservations/all/">My Reservations</a>
                     
                  </div>
                  </div>
            </div>
         </nav>
         <Routes>
            {/* place all your paths here */}
            <Route path="/signup/" element={<Signup />} />
            <Route path="/login/" element={<Login />} />
            <Route path="/reservations/all/" element={<><ReservationList /></>} />
            <Route path="/reservations/create/" element={<><CreateReservation /></>} />
            <Route path="/notifications/all/" element={<><NotificationList /></>} />
         </Routes>
         <br></br>
         {/* I couldn't figure out how to make the footer stay put at the bottom so currently this is commented out */}
         {/* <footer className="footerbar">
            <p className="footer_text">&copy; 2023 Restify.</p>
         </footer> */}
      </>
   );
};


export default App;
