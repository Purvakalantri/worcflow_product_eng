
import { useEffect, useState } from 'react'
import './Dashboard.css'
import Commitment from './Commitment'

function Dashboard() {

  const [commitments, setCommitments] = useState([])
  const [activeSection, setActiveSection] = useState('today')
  const [connectEmail, setConnectEmail] = useState(false)
  const [emailConnected, setEmailConnected] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {

    if(!connectEmail){
      return
    }
    setLoading(true)

    fetch('http://localhost:8000/api/get_commitments')
      .then((response) => response.json())
      .then((data) => {
        setCommitments(data.commitments)
        setEmailConnected(true)
      })
      .catch((error) => {
        console.error('Failed to fetch commitments:', error)
        setConnectEmail(false)
      })
      .finally(()=>{
        setLoading(false)
      })
  }, [connectEmail])

  // const addToCalendar = async (commitment) => {
  //   try {
  //     const response = await fetch('http://localhost:8000/api/calendar/add', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify(commitment),
  //     })
  
  //     const data = await response.json()
  
  //     console.log('Calendar event added:', data)
      

  //     window.open(data.event.event_link, '_blank')

  //   } catch (error) {
  //     console.error('Failed to add event to calendar:', error)
  //   }
  // }

  const addToCalendar = async (commitment) => {
    try {
      const response = await fetch('http://localhost:8000/api/calendar/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(commitment),
      })
  
      const data = await response.json()
  
      console.log('Calendar event added:', data)
  
      setCommitments((currentCommitments) =>
        currentCommitments.map((item) =>
          item.thread_id === commitment.thread_id
            ? {
                ...item,
                calendar: {
                  added: true,
                  event_id: data.event.event_id,
                  event_link: data.event.event_link,
                },
              }
            : item
        )
      )
    } catch (error) {
      console.error('Failed to add event to calendar:', error)
    }
  }

  const today = new Date().toISOString().split('T')[0]

  const todayCommitments = commitments.filter(
    (commitment) =>
      commitment.due_date && commitment.due_date === today
  )

  const futureCommitments = commitments.filter(
    (commitment) =>
      commitment.due_date && commitment.due_date > today
  )

  const pastCommitments = commitments.filter(
    (commitment) =>
      commitment.due_date && commitment.due_date < today
  )

  if (!emailConnected) {
    return (
      <div className="app">
        <div className="dashboard connect-screen">
          <h1>Worcflow AI</h1>
          <p>Commitment Tracker</p>
  
          <button
            className="connect-button"
            onClick={() => setConnectEmail(true)}
            disabled={loading}
          >
            {loading ? 'Connecting...' : 'Connect Your Email'}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="dashboard">

        <h1>Worcflow AI</h1>
        <p>Commitment Tracker</p>

        <div className="sections">

          <button
            className={activeSection === 'today' ? 'active' : ''}
            onClick={() => setActiveSection('today')}
          >
            Due Today
          </button>

          <button
            className={activeSection === 'future' ? 'active' : ''}
            onClick={() => setActiveSection('future')}
          >
            Future Dues
          </button>

          <button
            className={activeSection === 'past' ? 'active' : ''}
            onClick={() => setActiveSection('past')}
          >
            Past Dues
          </button>

        </div>

        <div className="content">

          {activeSection === 'today' && (
            <div>
              <h2>Due Today</h2>

              {todayCommitments.map((commitment) => (
                <Commitment
                  key={commitment.thread_id}
                  commitment={commitment}
                  onAddToCalendar={addToCalendar}
                />
              ))}
            </div>
          )}

          {activeSection === 'future' && (
            <div>
              <h2>Future Dues</h2>

              {futureCommitments.map((commitment) => (
                <Commitment
                  key={commitment.thread_id}
                  commitment={commitment}
                  onAddToCalendar={addToCalendar}
                />
              ))}
            </div>
          )}

          {activeSection === 'past' && (
            <div>
              <h2>Past Dues</h2>

              {pastCommitments.map((commitment) => (
                <Commitment
                  key={commitment.thread_id}
                  commitment={commitment} 
                  // onAddToCalendar={addToCalendar}
                />
              ))}
            </div>
          )}

        </div>

      </div>
    </div>
  )
}

export default Dashboard