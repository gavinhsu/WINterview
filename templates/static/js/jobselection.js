let occupation;
job = new Array();
job[0] = ["Hardware Engineer", "Software Engineer", "ML Engineer", "Database Administrator", "Data Scientist", "IT Specialist", "System Analyst", "System Engineer", "MIS Engineer", "Software Program Designer", "Software Testing Personnel", "Communications Engineer", "ERP Technical/Application Consultant", "Information Security Engineer", "Software QA Engineer", "Hardware QA Engineer", "Network Engineer", "Webmaster", "Website Programmer", "Computer Gaming Programmer", "	Electronics Engineer", "BIOS Engineer", "CIM Engineer"];
job[1] = ["Cashier", "Sales Trading", "Audit", "Quantitative", "Research", "Investment Banking", "	Finance Sales Personnel", "Financial Planning Personnel", "	Finance Researcher", "	Financial Analyst", "Treasury Specialist", "Accountant", "Cost Accounting Specialist", "Stock Broker", "Certified Investment Analyst", "Industrial Analyst", "	Loan/Credit Officer", "Actuary", "Account Collection Personnel", "Claim Adjuster", "Stock Affair Specialist", "Underwriting Personnel", "Bond Analyst", "Bond Trader"];

function renew(index) {
    occupation = index
    for (var i = 0; i < job[index].length; i++)
        document.selectjob.jobb.options[i] = new Option(job[index][i], job[index][i]);
    document.selectjob.jobb.length = job[index].length;
}


function isSelected(index) {

    var jobName;
    console.log(index)

    jobName = job[occupation][index];
    document.getElementById("jobName").value = jobName
    console.log(jobName)

}

$(document).ready(function () {
    $(".isSelected").prop('disabled', true);
    $('.selectJob').change(function () {
        if ($('.selectJob').val() == 0) {
            $(".isSelected").prop('disabled', true);
        } else {
            $(".isSelected").prop('disabled', false);
        }
    });
});