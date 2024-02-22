<div align="center">
    <img src="https://grow.empress.eco/uploads/default/original/2X/1/1f1e1044d3864269d2a613577edb9763890422ab.png" alt="Logo" width="80" height="80">
    <h3 align="center">Batch Payments</h3>
    <p align="center">
        Streamline your financial operations by handling multiple invoices with a single tool!
        <br />
        <a href="https://grow.empress.eco/"><strong>Explore the Docs »</strong></a>
        <br />
        <a href="https://github.com/empress-eco/batch_payments/issues">Report Bug or Request Feature</a>
    </p>
</div>

## About The Project

Batch Payments is a robust solution designed to simplify the process of managing multiple invoices. With its user-centric design, you can efficiently pay several purchase invoices in one go, generate an Australian Banking Association (ABA) file for outbound payments to various parties, and create and send remittance advice emails. 

### Key Features:

- Pay multiple purchase invoices in one batch
- Generate ABA files for outbound payments
- Send remittance advice emails to parties

## Technical Stack and Setup Instructions

Batch Payments is built on the solid foundation of the Framework. To get started with Batch Payments, follow the steps below:

1. Clone the repository: `git clone https://github.com/empress-eco/batch_payments.git`
2. Create a bank record and populate the `Financial Institution Abbreviation` custom field with a max 3 char abbreviation for the bank (e.g. CBA, ANZ).
3. Create a bank account linked to this bank, and populate the `Branch Code` with the BSB number in 000-000 format (e.g. 065-125).
4. Continue to populate the required fields as instructed [in the original instructions as given](https://gist.github.com/anonymous/7692091).

### Usage

The Batch Payment record will allow you to select a bank account for payments to be made from, select a date, select a posting date, and save the record. You can then filter suppliers and purchase invoices as required, select those you wish to pay, and create the payments. 

For more detailed instructions, please refer to the original instructions [here](https://gist.github.com/anonymous/7692091).

## Contribution Guidelines

We are excited about your interest in contributing to Batch Payments! Here's how you can help:

1. Fork the Project: `git clone https://github.com/empress-eco/batch_payments.git`
2. Create your Feature Branch: `git checkout -b feature/AmazingFeature`
3. Commit your Changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the Branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## License and Acknowledgements

### License

Batch Payments is licensed under the MIT License. Your contributions also fall under the MIT License.

### Acknowledgements

We express our deepest gratitude to the Empress Community for their invaluable contributions to the foundational tools that power this project. Their innovation and dedication have been instrumental in building the functionalities we rely on. We are profoundly grateful for their pioneering work and ongoing support.