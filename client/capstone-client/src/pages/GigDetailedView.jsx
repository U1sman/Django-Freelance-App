    import React from 'react';
    import { useEffect, useState } from 'react';
    import { useParams, Link } from 'react-router-dom';
    import Navbar from '../components/Navbar/Navbar';
    import CategoryScrollBar from '../components/CategoryScrollBar/CategoryScrollBar';

    const GigDetailedView = () => {

        const params = useParams();
        const [gig, setGig] = useState({});
        const fetchGig = async () =>{
            let response = await fetch(`http://127.0.0.1:8000/api/get_gig/${Number(params.gig_id)}/`, {
            method: 'GET',
            });
            let result = await response.json();
            setGig(result)
        };

        useEffect( () => {
        fetchGig()
        }, [Number(params.gig_id)]);

        return (
        <>

        <Navbar/>
        <CategoryScrollBar/>
        
        <div className="gigview_container">
            <p>in category/ <Link to={`/category/${gig.category?.name}`}>{gig.category?.name}</Link></p>
            <h2>{gig.title}</h2>
            <img src={`http://127.0.0.1:8000${gig.cover_image}`} alt="cover_image" />
            <h3>About this gig</h3>
            <p>{gig.description}</p>
        </div>

        </>
        )
    }

    export default GigDetailedView