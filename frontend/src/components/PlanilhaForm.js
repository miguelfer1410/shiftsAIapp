import React, { useState } from 'react';
import axios from 'axios';

const PlanilhaForm = () => {
    const [description, setDescription] = useState('');
    const [fileUrl, setFileUrl] = useState('');
  
    const handleGenerateSchedule = async () => {
        try {
            const response = await axios.post('http://localhost:5000/generate_schedule', {description}, {
                responseType: 'blob'
            });

            console.log(response);
            
    
            // Create a link element to trigger the download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'schedule.xlsx'); // Specify the file name
            document.body.appendChild(link);
            link.click(); // Trigger the download
            document.body.removeChild(link); // Clean up
        } catch (error) {
            console.error('Error generating schedule:', error);
        }
    };
  
    return (
      <div className="App">
        <h1>Work Schedule Generator</h1>
        <textarea
          rows="10"
          cols="50"
          placeholder="Describe the schedule here"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <br />
        <button onClick={handleGenerateSchedule}>Generate Schedule</button>
        {fileUrl && (
          <div>
            <a href={fileUrl} download="work_schedule.xlsx">Download Schedule</a>
          </div>
        )}
      </div>
    );
};

export default PlanilhaForm;
