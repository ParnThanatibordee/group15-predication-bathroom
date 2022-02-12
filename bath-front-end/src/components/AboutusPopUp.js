import React from 'react'

const AboutusPopUp = (props) => {
    return (props.trigger) ? (
        <div className="popup">
            <div className="popupInner">
                <button className="close-btn" onClick={props.closePopup}>Close</button>
                {props.children}
            </div>
        </div>
    ) : "";
}

export default AboutusPopUp