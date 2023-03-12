import React, {useContext} from 'react';
import { AuthContext } from '../context/auth_context';
import '../stylesheets/Home.css';

function Home() {
const { auth, authDispatch } = useContext(AuthContext);
  return (
    <div className="home-page">
      <h1>Welcome {auth.username}!</h1>
    </div>
  );
}

export default Home;
