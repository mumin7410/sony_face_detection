import React, {useState, useEffect} from "react";
const Box = () => {

    const [Data, setData] = useState([]);
    useEffect(() => {
      fetch(`http://127.0.0.1:8000/api/Members`)
      .then((response) => response.json())
      .then((actualData) => setData(actualData))
    }, []);

    return(
        <>
            <div className='flex min-h-[100vh] bg-[#232E37] px-[150px] py-[50px]'>
            {Data.map((i,index) => {
                return(
                <div className='flex flex-col py-[20px] px-[50px] m-[10px] bg-[#313E4A] rounded-2xl w-[400px] h-[250px] justify-center'>
                    <p>Name: {i.Name}</p>
                    <p>Status: {i.Active ? "Active" : "Inactive"}</p>
                    <p>Location: {i.Location}</p>
                    <p>Time: {i.date_time}</p>
                </div>
                )
            })}
            </div>
        </>
    )
}

export default Box;