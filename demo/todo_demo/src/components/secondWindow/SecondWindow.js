import React from 'react';
import {useParams} from 'react-router-dom';

function SecondWindow(){
    const params = useParams();
    console.log(params);
    return(
        <p>This is SecondWindow!</p>
    )
}
export default SecondWindow;