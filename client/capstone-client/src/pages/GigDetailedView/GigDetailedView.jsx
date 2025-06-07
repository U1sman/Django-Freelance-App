    import React from 'react';
    import { useEffect, useState } from 'react';
    import { useParams, Link } from 'react-router-dom';
    import Navbar from '../../components/Navbar/Navbar';
    import CategoryScrollBar from '../../components/CategoryScrollBar/CategoryScrollBar';
    import styles from './GigDetailedView.module.scss'

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

        console.log(gig.related_seller);
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
            <div className="pricingPlan">
                {gig?.pricing_plan?.pricing_options.map((pricingOption)=>{
                    return(
                        <div className={styles.pricingOption} key={pricingOption.id}>
                            <p>type: {pricingOption.type}</p>
                            <p>price: {pricingOption.price}</p>
                            <p>description: {pricingOption.description}</p>
                            <p>delivery_time: {pricingOption.delivery_time}</p>
                        </div>
                    )
                })}
            </div>
            <p>Get to know the Seller</p>
            <div className="sellerInfoBox">
                <img src={`http://127.0.0.1:8000${gig.related_seller?.profile_pic}`} alt="profile_pic" />
                <p>{gig.related_seller?.username}</p>
                <p>{gig.related_seller?.tagline}</p>
                <div className="ratingInfo">
                    this is a placeholder for the ratings and stuff
                </div>
                <p>from: {gig.related_seller?.country_name}</p>
                <p>Member Since: {gig.related_seller?.joined_date}</p>

            </div>
        </div>

        </>
        )
    }

    export default GigDetailedView