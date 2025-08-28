// Custom Tailwind classes and component styles
export const styles = {
  // Layout
  container: "min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 font-sans",
  mainContent: "relative h-screen flex items-center justify-center px-4",
  contentWrapper: "text-center max-w-4xl min-w-[600px] mx-auto",
  
  // Header
  header: "text-center mb-8",
  title: "text-4xl font-semibold text-gray-800 mb-2 tracking-tight",
  subtitle: "text-lg text-gray-600 max-w-2xl mx-auto",
  
  // Form
  form: "mb-8",
  inputWrapper: "w-full relative mb-4",
  urlInput: "h-12 w-full px-4 text-base border border-gray-300 rounded-lg outline-none bg-white shadow-sm transition-all duration-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 disabled:opacity-50",
  submitButton: "absolute right-2 top-1/2 transform -translate-y-1/2 h-8 px-4 bg-blue-500 text-white border-none rounded-md text-sm font-medium cursor-pointer transition-all duration-200 flex items-center gap-2 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed",
  
  // Advanced Options
  advancedToggle: "bg-transparent border-none text-blue-500 text-sm cursor-pointer underline p-2",
  advancedPanel: "bg-white rounded-lg p-6 mb-8 shadow-sm border border-gray-200 text-left",
  advancedTitle: "text-base font-semibold text-gray-800 mb-4",
  label: "block text-sm font-medium text-gray-700 mb-2",
  textarea: "w-full min-h-[60px] p-3 border border-gray-300 rounded-md text-sm resize-vertical font-sans",
  textareaMonospace: "w-full min-h-[120px] p-3 border border-gray-300 rounded-md text-sm resize-vertical font-mono",
  helpText: "text-xs text-gray-500 mt-2",
  
  // Progress
  progressContainer: "mb-8",
  progressBar: "w-full h-1 bg-gray-200 rounded-full overflow-hidden mb-2",
  progressFill: "h-full bg-gradient-to-r from-blue-500 to-purple-500 animate-progress w-1/3",
  progressText: "text-center text-gray-600 text-sm",
  
  // Error
  errorContainer: "bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg flex items-center gap-2 mb-8",
  
  // Alternative Options
  divider: "text-center my-6 relative",
  dividerText: "bg-gradient-to-br from-gray-50 to-gray-100 px-4 text-gray-500 text-sm",
  fileUpload: "text-center",
  fileUploadButton: "inline-block p-3 bg-white border-2 border-dashed border-gray-300 rounded-lg text-gray-600 text-sm cursor-pointer transition-all duration-200 hover:border-blue-500 hover:bg-blue-50",
  fileUploadText: "text-gray-500 text-xs mt-2",
  
  // Examples
  examplesContainer: "text-center",
  examplesTitle: "text-base font-medium text-gray-700 mb-4",
  examplesGrid: "flex gap-2 justify-center flex-wrap",
  exampleButton: "p-2 bg-white border border-gray-300 rounded-md text-gray-600 text-sm cursor-pointer transition-all duration-200 hover:bg-gray-50 hover:border-gray-400",
  
  // Swagger UI
  swaggerContainer: "p-6",
  swaggerHeader: "flex justify-between items-center mb-6",
  swaggerTitle: "text-2xl font-semibold text-gray-800",
  resetButton: "btn-secondary",
  
  // Loading States
  loadingSpinner: "animate-spin",
  loadingText: "text-gray-600 text-sm",
  
  // Animations
  fadeIn: "animate-fadeIn",
  
  // Responsive
  responsive: {
    mobile: "min-w-[320px] max-w-full",
    tablet: "min-w-[600px]",
    desktop: "min-w-[800px]"
  }
};

// Component-specific styles
export const componentStyles = {
  homeScreen: {
    container: styles.container,
    mainContent: styles.mainContent,
    contentWrapper: `${styles.contentWrapper} ${styles.responsive.desktop}`,
    header: styles.header,
    title: styles.title,
    subtitle: styles.subtitle,
    form: styles.form,
    inputWrapper: styles.inputWrapper,
    urlInput: styles.urlInput,
    submitButton: styles.submitButton,
    advancedToggle: styles.advancedToggle,
    advancedPanel: styles.advancedPanel,
    advancedTitle: styles.advancedTitle,
    label: styles.label,
    textarea: styles.textarea,
    textareaMonospace: styles.textareaMonospace,
    helpText: styles.helpText,
    progressContainer: styles.progressContainer,
    progressBar: styles.progressBar,
    progressFill: styles.progressFill,
    progressText: styles.progressText,
    errorContainer: styles.errorContainer,
    divider: styles.divider,
    dividerText: styles.dividerText,
    fileUpload: styles.fileUpload,
    fileUploadButton: styles.fileUploadButton,
    fileUploadText: styles.fileUploadText,
    examplesContainer: styles.examplesContainer,
    examplesTitle: styles.examplesTitle,
    examplesGrid: styles.examplesGrid,
    exampleButton: styles.exampleButton
  },
  
  swaggerView: {
    container: styles.swaggerContainer,
    header: styles.swaggerHeader,
    title: styles.swaggerTitle,
    resetButton: styles.resetButton
  }
};
