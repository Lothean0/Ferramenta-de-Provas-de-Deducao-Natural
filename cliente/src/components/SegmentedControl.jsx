import React from "react";
import "../styles/SegmentedControl.css";

const SegmentedControl = ({ onChange }) => {
  return (
    <div className="segmented-control">
      <input 
        type="radio" 
        name="radio2" 
        value="PT" 
        id="tab-1" 
        defaultChecked 
        onChange={() => onChange('PT')} 
      />
      <label htmlFor="tab-1" className="segmented-control__1">
        PT
      </label>

      <input 
        type="radio" 
        name="radio2" 
        value="EN" 
        id="tab-2" 
        onChange={() => onChange('EN')} 
      />
      <label htmlFor="tab-2" className="segmented-control__2">
        EN
      </label>

      <div className="segmented-control__color"></div>
    </div>
  );
};

export default SegmentedControl;
