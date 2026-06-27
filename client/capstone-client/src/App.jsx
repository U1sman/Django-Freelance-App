import BrowseGigs from "./pages/BrowseGigs/BrowseGigs";
import Login from "./pages/Login/Login";
import Signup from "./pages/Signup/Signup";
import BrowseCategoryGigs from "./pages/BrowseCategoryGigs/BrowseCategoryGigs";
import GigDetailedView from "./pages/GigDetailedView/GigDetailedView";
import ProvideRequirements from "./pages/ProvideRequirements/ProvideRequirements";
import Checkout from "./pages/Checkout/Checkout";
import Order from "./pages/Order/Order";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';


function App() {

  const router = createBrowserRouter([
  {
    path:"/",
    element: <BrowseGigs/>
  },

  {
    path:"/login",
    element: <Login/>
  },

  {
    path:"/signup",
    element: <Signup/>
  },

  {
    path:"/category/:categoryName",
    element: <BrowseCategoryGigs/>
  },

  {
    path:"/gig/:gig_id",
    element: <GigDetailedView/>
  },

  {
    path:"/gig/:gig_id/provideRequirements/:pricingOptionId",
    element: <ProvideRequirements/>
  },

  {
    path:"/gig/:gig_id/checkout",
    element: <Checkout/>
  },

  {
    path:"order/:order_id",
    element: <Order/>
  }
  ])

  return (
    <>
      <RouterProvider router={router}/>
    </>
  )
}

export default App
