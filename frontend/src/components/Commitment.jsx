
import './Commitment.css'

function Commitment({ commitment, onAddToCalendar }) {
    return (
      <div className="commitment-card">
  
        <h3>{commitment.task}</h3>
  
        <div className="commitment-info">
          <p><span>To:</span> {commitment.recipient_name}</p>
  
          <p><span>Email:</span> {commitment.recipient_email}</p>
  
          <p><span>Due:</span> {commitment.due_date || "No due date"}</p>
        
        </div>
  
        {commitment.requirements?.length > 0 && (
          <div className="requirements">
            <p>Requirements:</p>
  
            
              {commitment.requirements.map((requirement, index) => (
                <li key={index}>{requirement}</li>
              ))}
            
          </div>
        )}
  
        <p className="status">
          Status: {commitment.status}
        </p>

        {commitment.due_date && onAddToCalendar &&(
          <button
            className="calendar-button"
            onClick={() => {
              if (commitment.calendar?.added) {
                window.open(commitment.calendar.event_link, '_blank')
              } else {
                onAddToCalendar(commitment)
              }
            }}
          >
            {commitment.calendar?.added
              ? '✓ Added to Calendar Check out'
              : 'Add to Calendar'}
        </button>
      )}
  
      </div>
    );
  }
  
  export default Commitment;