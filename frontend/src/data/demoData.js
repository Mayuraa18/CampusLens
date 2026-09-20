export const starterDocuments = [
  { id: 1, title: 'Bharat Builds Tour — Student Guide', type: 'Event guide', date: 'Today', pages: 6, color: 'lime', status: 'Ready', summary: 'Everything you need for the Bharat Builds Tour: schedule, challenge tracks and what to bring.' },
  { id: 2, title: 'End Semester Examination Circular', type: 'Academic notice', date: 'Yesterday', pages: 4, color: 'sand', status: 'Ready', summary: 'Registration instructions, fee payment information and examination dates.' },
  { id: 3, title: 'Scholarship Opportunities 2026', type: 'Opportunity', date: '12 Sep', pages: 8, color: 'coral', status: 'Processing', summary: 'A collection of scholarships with eligibility and application deadlines.' },
]

export const dashboardTasks = [
  { title: 'Bring your laptop to Bharat Builds', date: 'Today', tone: 'lime' },
  { title: 'Check examination registration', date: '20 Oct', tone: 'sand' },
  { title: 'Review scholarship eligibility', date: '28 Sep', tone: 'coral' },
]

export const starterMessages = [
  { role: 'assistant', text: 'Hi Mayura! I’ve read the Bharat Builds Tour guide. What would you like to know?', time: 'Now' },
  { role: 'user', text: 'What should I bring to the hackathon?', time: 'Now' },
  { role: 'assistant', text: 'Bring a laptop and charger, your student ID, a reusable water bottle, and your best project idea. Registration begins at 9:00 AM.', time: 'Now', source: 'Source · Page 2' },
]
